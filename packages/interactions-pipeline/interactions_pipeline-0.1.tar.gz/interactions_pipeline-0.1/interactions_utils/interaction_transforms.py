import dateutil
from apache_beam.transforms import PTransform, ParDo, DoFn


class _PairWithDeliveryId(DoFn):

    def process(self, element):

        keys = ['received_occurred_at', 'occurred_at']

        for key in keys:
            if key in element:
                try:
                    element[key] = dateutil.parser.parse(element[key])
                except:
                    pass
        try:
            if 'delivery_id' in element:
                return [(element['delivery_id'], element), ]
            else:
                return [(element['data']['properties']['delivery_id'], element), ]
        except Exception as e:
            return None


class PairWithDeliveryId(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_PairWithDeliveryId())


class _PairWithLoadIdPersonId(DoFn):

    def process(self, element):

        keys = ['timestamp']

        for key in keys:
            if key in element:
                try:
                    element[key] = dateutil.parser.parse(element[key])
                except:
                    pass
        try:
            key = (element["person_id"] + "_" + element["loadId"]).decode("utf-8")
            return [(key, element), ]
        except Exception as e:
            return None


class PairWithLoadIdPersonId(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_PairWithLoadIdPersonId())


class _CreateEmailPersonIdLoadIdPairs(DoFn):

    def process(self, element):

        # Split out element pair
        key, data = element

        # Get all receives, opens and clicks
        received_emails = data["received_emails"]
        opened_emails = data["opened_emails"]
        clicked_emails = data["clicked_emails"]

        # since each was groupby before cogroupby all elements in first list entry
        if received_emails:
            received_emails = received_emails[0]

        if opened_emails:
            opened_emails = opened_emails[0]

        if clicked_emails:
            clicked_emails = clicked_emails[0]

        # Create an entry for each load in original receive
        drip_event_list = []
        received_emails = list(received_emails)

        # If received emails event
        if received_emails:
            if received_emails[0]["load_id_0"]:
                received_dict = {
                    "key": str(received_emails[0]["person_id"]) + "_" + str(received_emails[0]["load_id_0"]),
                    "email_received_at": received_emails[0]["received_occurred_at"],
                    "automation_name": received_emails[0]["automation_name"],
                    "load_link": received_emails[0]["load_link_0"],
                    "match_link": received_emails[0]["match_link_0"],
                    "email_opens": [],
                    "email_clicks": []
                }
                drip_event_list.append(received_dict)

            if received_emails[0]["load_id_1"]:
                received_dict = {
                    "key": str(received_emails[0]["person_id"]) + "_" + str(received_emails[0]["load_id_1"]),
                    "email_received_at": received_emails[0]["received_occurred_at"],
                    "automation_name": received_emails[0]["automation_name"],
                    "load_link": received_emails[0]["load_link_1"],
                    "match_link": received_emails[0]["match_link_1"],
                    "email_opens": [],
                    "email_clicks": []
                }
                drip_event_list.append(received_dict)

            if received_emails[0]["load_id_2"]:
                received_dict = {
                    "key": str(received_emails[0]["person_id"]) + "_" + str(received_emails[0]["load_id_2"]),
                    "email_received_at": received_emails[0]["received_occurred_at"],
                    "automation_name": received_emails[0]["automation_name"],
                    "load_link": received_emails[0]["load_link_2"],
                    "match_link": received_emails[0]["match_link_2"],
                    "email_opens": [],
                    "email_clicks": []
                }
                drip_event_list.append(received_dict)

        # Add opens and clicks for each receive load link
        for drip_event in drip_event_list:

            # Add click event for corresponding load
            for click in clicked_emails:
                if drip_event["load_link"] in click["data"]["properties"]["url"] or \
                        drip_event["match_link"] in click["data"]["properties"]["url"]:
                    drip_event["email_clicks"].append(click["occurred_at"])

            # Add open to each load
            for open in opened_emails:
                drip_event["email_opens"].append(open["occurred_at"])

            drip_event["email_clicks"].sort()
            drip_event["email_clicks"] = [x.isoformat() for x in drip_event["email_clicks"]]
            drip_event["email_opens"].sort()
            drip_event["email_opens"] = [x.isoformat() for x in drip_event["email_opens"]]

            yield (drip_event["key"].decode('utf-8'), drip_event)


class CreateEmailPersonIdLoadIdPairs(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateEmailPersonIdLoadIdPairs())


class _CreateInteractions(DoFn):

    def process(self, element):

        # Split out element pair
        key, data = element

        # Create dict structure for all interactions
        interaction_dict = {
            "person_id": key.split("_")[0],
            "load_id": key.split("_")[1],
            "email_interactions": [],
            "open_load_details": [],
            "liked_a_load": [],
            "contact_button_clicked": [],
            "load_booked": []
        }

        # Get Drip and MixPanel Events
        drip_event_list = data["drip"]
        mix_panel_event_list = data["mixpanel"]

        # Since each was groupby before cogroupby all elements in first list entry
        if drip_event_list:
            drip_event_list = drip_event_list[0]

        if mix_panel_event_list:
            mix_panel_event_list = mix_panel_event_list[0]

        # Put mixpanel and drip events into list
        mix_panel_event_list = list(mix_panel_event_list)
        drip_event_list = list(drip_event_list)

        # Sort Drip events by email_received
        if drip_event_list:
            drip_event_list.sort(key=lambda item: item['email_received_at'], reverse=False)

            # Insert Drip Events
            for drip_event in drip_event_list:
                del drip_event["key"]
                drip_event["email_received_at"] = drip_event["email_received_at"].isoformat()
                interaction_dict["email_interactions"].append(drip_event)

        # Parse the mix panel events
        for mix_panel_event in mix_panel_event_list:
            if mix_panel_event["event_type"] == u"Opened Load Details":
                interaction_dict["open_load_details"].append(mix_panel_event["timestamp"])
            elif mix_panel_event["event_type"] == u"Liked a Load":
                interaction_dict["liked_a_load"].append(mix_panel_event["timestamp"])
            elif mix_panel_event["event_type"] == u"Book Confirm Clicked":
                interaction_dict["load_booked"].append(mix_panel_event["timestamp"])
            elif mix_panel_event["event_type"] == u"Contact Button Clicked":
                interaction_dict["contact_button_clicked"].append(mix_panel_event["timestamp"])

        # Sort Lists, Convert to BQ Format
        interaction_dict["open_load_details"] = list(dict.fromkeys(interaction_dict["open_load_details"]))
        interaction_dict["open_load_details"].sort()
        interaction_dict["open_load_details"] = [x.isoformat() for x in interaction_dict["open_load_details"]]

        interaction_dict["liked_a_load"] = list(dict.fromkeys(interaction_dict["liked_a_load"]))
        interaction_dict["liked_a_load"].sort()
        interaction_dict["liked_a_load"] = [x.isoformat() for x in interaction_dict["liked_a_load"]]

        interaction_dict["load_booked"] = list(dict.fromkeys(interaction_dict["load_booked"]))
        interaction_dict["load_booked"].sort()
        interaction_dict["load_booked"] = [x.isoformat() for x in interaction_dict["load_booked"]]

        interaction_dict["contact_button_clicked"] = list(dict.fromkeys(interaction_dict["contact_button_clicked"]))
        interaction_dict["contact_button_clicked"].sort()
        interaction_dict["contact_button_clicked"] = [x.isoformat() for x in interaction_dict["contact_button_clicked"]]

        return [interaction_dict, ]


class CreateInteractions(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateInteractions())


class _CreateUserItemMatrix(DoFn):

    def process(self, interaction_dict):

        # Build out Scoring System
        # Booked is 5*
        # Contact is 4.5*
        # Load Opened more than 3 times is 4* Opened less than 3 is 3.5*
        # Email Click is 3.5*
        # Email Open is 2.5*
        # Email Received with no interaction is 1*

        score = None

        if len(interaction_dict["load_booked"]) > 0:
            score = 5
        elif len(interaction_dict["contact_button_clicked"]) > 0:
            score = 4.5
        elif len(interaction_dict["open_load_details"]) > 0:
            if len(interaction_dict["open_load_details"]) >= 3:
                score = 4
            else:
                score = 3.5

        # elif email interactions exists
        elif len(interaction_dict["email_interactions"]) > 1:
            # At least 1* for receiving an email
            score = 1
            for email_interaction in interaction_dict["email_interactions"]:
                if len(email_interaction["email_clicks"]) > 0:
                    score = 3.5
                    break
                elif len(email_interaction["email_opens"]) > 0:
                    score = 2.5

        score_dict = {
            "person_id": interaction_dict["person_id"],
            "load_id": interaction_dict["load_id"],
            "score": score
        }

        return [score_dict, ]


class CreateUserItemMatrix(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_CreateUserItemMatrix())
