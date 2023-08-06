from apache_beam.transforms import PTransform, ParDo, DoFn
import collections
import datetime


def transform_list_fields(source_dict, source_field, output_dict, output_field):
    """"""
    list = [x.upper() for x in source_dict[source_field]]
    string = ', '.join(map(str, list))
    output_dict[output_field] = string

    return output_dict


class _TransformUsers(DoFn):

    def process(self, element):

        # Transform the doc into Big Query Format
        transformed_doc = collections.OrderedDict()

        transformed_doc['mongo_id'] = str(element['_id'])

        transformed_doc['firebaseUID'] = str(element['firebaseUID'])

        try:
            transformed_doc['phone'] = str(element['phone'])
        except Exception:
            transformed_doc['phone'] = None

        # Convert Time Stamp
        try:
            element['creationTimestamp'] = int(element['creationTimestamp'])
        except Exception:
            element['creationTimestamp'] = 0

        if len(str(abs(element['creationTimestamp']))) == 10:
            transformed_doc['creation_timestamp'] = datetime.datetime.utcfromtimestamp(element['creationTimestamp'])\
                .isoformat()
        elif len(str(abs(element['creationTimestamp']))) == 13:
            transformed_doc['creation_timestamp'] = \
                datetime.datetime.utcfromtimestamp(element['creationTimestamp']/1000).isoformat()
        else:
            transformed_doc['creation_timestamp'] = datetime.datetime(1970, 1, 1, 0, 0, 0, 0).isoformat()

        try:
            transformed_doc['display_name'] = str(element['displayName'])
        except Exception:
            transformed_doc['display_name'] = None

        try:
            transformed_doc['disabled'] = bool((element['disabled']))
        except Exception:
            transformed_doc['disabled'] = None

        try:
            transformed_doc['email'] = str(element['email'])
            if transformed_doc['email'] in ["None", ""]:
                transformed_doc['email'] = None
        except Exception:
            transformed_doc['email'] = None

        try:
            transformed_doc['email_verified'] = bool((element['emailVerified']))
        except Exception:
            transformed_doc['email_verified'] = None

        try:
            transformed_doc['user_type'] = str(element['userType'])
        except Exception:
            transformed_doc['user_type'] = None

        if 'equipmentTypeList' not in element:
            element['equipmentTypeList'] = []
        transformed_doc = transform_list_fields(element, 'equipmentTypeList', transformed_doc, 'equipment_types')

        try:
            transformed_doc['credit_card_rating'] = int(element['creditCardRating'])
        except Exception:
            transformed_doc['credit_card_rating'] = None

        try:
            transformed_doc['truck_type'] = str(element['truckType'])
        except Exception:
            transformed_doc['truck_type'] = None

        try:
            transformed_doc['preferred_per_mile_price'] = float(element['preferredPerMileRate']['price'])
        except Exception:
            transformed_doc['preferred_per_mile_price'] = None

        try:
            transformed_doc['preferred_per_mile_currency'] = str(element['preferredPerMileRate']['currency'])
        except Exception:
            transformed_doc['preferred_per_mile_currency'] = None

        try:
            transformed_doc['office_phone'] = str(element['officePhone'])
        except Exception:
            transformed_doc['office_phone'] = None

        try:
            transformed_doc['company_name'] = str(element['companyName'])
        except Exception:
            transformed_doc['company_name'] = None

        try:
            transformed_doc['company_type'] = str(element['companyType'])
        except Exception:
            transformed_doc['company_type'] = None

        try:
            transformed_doc['address_state'] = str(element['address']['state'])
        except Exception:
            transformed_doc['address_state'] = None

        try:
            transformed_doc['address_city'] = str(element['address']['city'])
        except Exception:
            transformed_doc['address_city'] = None

        try:
            transformed_doc['address_postal_code'] = str(element['address']['postalCode'])
        except Exception:
            transformed_doc['address_postal_code'] = None

        try:
            transformed_doc['address_line1'] = str(element['address']['line1'])
        except Exception:
            transformed_doc['address_line1'] = None

        try:
            transformed_doc['address_line2'] = str(element['address']['line2'])
        except Exception:
            transformed_doc['address_line2'] = None

        try:
            transformed_doc['address_coordinate_lat'] = float(element['address']['coordinate']['lat'])
        except Exception:
            transformed_doc['address_coordinate_lat'] = None

        try:
            transformed_doc['address_coordinate_lon'] = float(element['address']['coordinate']['lon'])
        except Exception:
            transformed_doc['address_coordinate_lon'] = None

        try:
            transformed_doc['mc_number'] = str(element['mcNumber'])
        except Exception:
            transformed_doc['mc_number'] = None

        try:
            operating_lanes = element["operatingLanes"]
        except Exception:
            operating_lanes = []

        for i in range(5):
            try:
                transformed_doc["operating_lanes_" + str(i+1) + "_pickup_country"] = operating_lanes[i]["pickup"]["country"]
                transformed_doc["operating_lanes_" + str(i+1) + "_pickup_state"] = operating_lanes[i]["pickup"]["state"]
                transformed_doc["operating_lanes_" + str(i+1) + "_pickup_city"] = operating_lanes[i]["pickup"]["city"]
                transformed_doc["operating_lanes_" + str(i+1) + "_dropoff_country"] = operating_lanes[i]["dropoff"]["country"]
                transformed_doc["operating_lanes_" + str(i+1) + "_dropoff_state"] = operating_lanes[i]["dropoff"]["state"]
                transformed_doc["operating_lanes_" + str(i+1) + "_dropoff_city"] = operating_lanes[i]["dropoff"]["city"]
            except Exception:
                transformed_doc["operating_lanes_" + str(i+1) + "_pickup_country"] = None
                transformed_doc["operating_lanes_" + str(i+1) + "_pickup_state"] = None
                transformed_doc["operating_lanes_" + str(i+1) + "_pickup_city"] = None
                transformed_doc["operating_lanes_" + str(i+1) + "_dropoff_country"] = None
                transformed_doc["operating_lanes_" + str(i+1) + "_dropoff_state"] = None
                transformed_doc["operating_lanes_" + str(i+1) + "_dropoff_city"] = None

        try:
            transformed_doc['communications_preferences_recommendations'] = bool(
                element['communicationsPreferences']['recommendations'])
        except Exception:
            transformed_doc['communications_preferences_recommendations'] = None

        try:
            transformed_doc['agreed_to_terms_and_conditions_bool'] = bool(
                element['agreedToTermsAndConditions']['agreedToTermsAndConditions'])
        except Exception:
            transformed_doc['agreed_to_terms_and_conditions_bool'] = None

        # Convert TimeStamp
        try:
            if len(str(abs(element['agreedToTermsAndConditions']['time_signed']))) == 10:
                transformed_doc['agreed_to_terms_and_conditions_timestamp'] = datetime.datetime.utcfromtimestamp(
                    int(element['agreedToTermsAndConditions']['time_signed'])).isoformat()
            elif len(str(abs(element['agreedToTermsAndConditions']['time_signed']))) == 13:
                transformed_doc['agreed_to_terms_and_conditions_timestamp'] = \
                    datetime.datetime.utcfromtimestamp(int(element['agreedToTermsAndConditions']['time_signed']) / 1000).isoformat()
            else:
                transformed_doc['agreed_to_terms_and_conditions_timestamp'] = None
        except Exception:
             transformed_doc['agreed_to_terms_and_conditions_timestamp'] = None

        try:
            transformed_doc['first_login'] = bool(element['firstLogin'])
        except Exception:
            transformed_doc['first_login'] = None

        try:
            transformed_doc['channel'] = str(element['channel'])
        except Exception:
            transformed_doc['channel'] = None

        try:
            transformed_doc['truck_count'] = int(element['truckCount'])
        except Exception:
            transformed_doc['truck_count'] = None

        try:
            if isinstance(element['lastLogin'], datetime.datetime):
                transformed_doc['last_login'] = element['last_login'].isoformat()
            else:
                transformed_doc['last_login'] = datetime.datetime(1970, 1, 1, 0, 0, 0, 0).isoformat()
        except Exception:
            transformed_doc['last_login'] = None

        try:
            transformed_doc['dispatchable'] = str(element['dispatchable'])
        except Exception:
            transformed_doc['dispatchable'] = None

        try:
            if 'preferredLanes' not in element or element['preferredLanes'] is None:
                element['preferredLanes'] = {"states": []}

            if 'states' not in element['preferredLanes']:
                element['preferredLanes']['states'] = []
            transformed_doc = transform_list_fields(element['preferredLanes'],
                                                    'states',
                                                    transformed_doc,
                                                    'preferred_lanes')
        except Exception:
            transformed_doc['states'] = None

        try:
            transformed_doc['skip_onboarding'] = bool(element['preferredLanes']['skipOnboarding'])
        except Exception:
            transformed_doc['skip_onboarding'] = None

        try:
            transformed_doc['follow_money'] = bool(element['preferredLanes']['followMoney'])
        except Exception:
            transformed_doc['follow_money'] = None

        return [transformed_doc, ]


class TransformUsers(PTransform):

    def expand(self, pcoll):
        return pcoll | ParDo(_TransformUsers())
