# pytype: skip-file
from __future__ import absolute_import
from __future__ import division
import apache_beam as beam
import datetime
import logging
from google.cloud import bigquery
logger = logging.getLogger(__name__)


def get_equipment_type_list(load_obj):
    result = []
    for load in load_obj["payload"]["loads"]:
        for key in [
            "auto",
            "hopperBottom",
            "reefer",
            "tanker",
            "van",
            "dumpTruck",
            "powerOnly",
            "container",
        ]:
            if load["loadContentDetails"]["equipmentTypes"][key]:
                result.append(key)

        for key in ["movingVan", "boatHauler", "heavyHaulers", "animalCarrier"]:
            if load["loadContentDetails"]["equipmentTypes"]["specialized"][key]:
                result.append(key)

        for key in [
            "landoll",
            "removableGooseneck",
            "doubleDrop",
            "lowboy",
            "flatbed",
            "maxi",
            "stepDeck",
        ]:
            if load["loadContentDetails"]["equipmentTypes"]["flatbed"][key]:
                result.append(key)

    return [i.upper() for i in set(result)]


def _get_date_string_delta(date, days=0, hours=0, minutes=0):
    """"""
    date_delta = date - datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return date_delta


def _get_last_assigned_date_in_bq_table(project, table):
    """"""
    client = bigquery.Client()

    # Create BigQuery Query
    query = 'SELECT assigned_date FROM `{}.{}`' \
          ' ORDER BY assigned_date DESC LIMIT 1'.format(project, table)

    # Perform a query.
    query_job = client.query(query)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        timestamp = row['assigned_date']

    return timestamp


def create_assigned_date_mongo_query(gcp_project, bq_table, minutes=5):
    """"""
    assigned_date = _get_last_assigned_date_in_bq_table(gcp_project, bq_table)
    filter_date = _get_date_string_delta(assigned_date, minutes=minutes)
    query = {'payload.assignedDate': {u"$gt": filter_date}}
    return query


class _TransformLoads(beam.DoFn):

    def process(self, element):
        import collections
        import datetime

        # Transform the doc into Big Query Format
        transformed_doc = collections.OrderedDict()

        transformed_doc['mongo_id'] = str(element['_id'])

        # Get Source
        try:
            transformed_doc["source"] = str(element["source"])
        except Exception:
            transformed_doc["source"] = None

        # Get Pickup Start Date
        try:
            transformed_doc["pickup_start_date"] = element["payload"]["tripDetails"]['pickupStartDate']
        except Exception:
            transformed_doc["pickup_start_date"] = None

        # Get Pickup End Date
        try:
            transformed_doc["pickup_end_date"] = element["payload"]["tripDetails"]['pickupEndDate']
        except Exception:
            transformed_doc["pickup_end_date"] = transformed_doc["pickup_start_date"]

        # Get Pickup Start Time
        try:
            pickup_start_time = datetime.datetime.strptime(element["payload"]["tripDetails"]['pickupStartTime'], '%I:%M %p').time()
        except Exception:
            pickup_start_time = None

        # Get Pickup End Time
        try:
            pickup_end_time = datetime.datetime.strptime(element["payload"]["tripDetails"]['pickupEndTime'], '%I:%M %p').time()
        except Exception:
            pickup_end_time = None

        # Add time to dates
        if pickup_start_time and transformed_doc["pickup_start_date"]:

            try:
                transformed_doc["pickup_start_date"] = transformed_doc["pickup_start_date"].replace(
                    hour=pickup_start_time.hour,
                    minute=pickup_start_time.minute
                )

            # If error use date as a datetime
            except Exception:
                pass

        try:
            transformed_doc["pickup_start_date"] = transformed_doc["pickup_start_date"].isoformat()
        except Exception:
            transformed_doc["pickup_start_date"] = None

        # Add time to dates
        if pickup_end_time and transformed_doc["pickup_end_date"]:

            try:
                transformed_doc["pickup_end_date"] = transformed_doc["pickup_end_date"].replace(
                    hour=pickup_end_time.hour,
                    minute=pickup_end_time.minute
                )

            # If error use date as a datetime
            except Exception as e:
                pass

        try:
            transformed_doc["pickup_end_date"] = transformed_doc["pickup_end_date"].isoformat()
        except Exception:
            transformed_doc["pickup_end_date"] = None

        # Get Pickup Start Lat
        try:
            transformed_doc["pickup_lat"] = float(element["payload"]["tripDetails"]['pickupCoordinates']['lat'])
        except Exception:
            transformed_doc["pickup_lat"] = None

        # Get Pickup Start Lon
        try:
            transformed_doc["pickup_lon"] = float(element["payload"]["tripDetails"]['pickupCoordinates']['lng'])
        except Exception:
            transformed_doc["pickup_lon"] = None

        # Get Pickup Country
        try:
            transformed_doc["pickup_country"] = str(element["payload"]["tripDetails"]["pickupAddress"]["country"])
        except Exception:
            transformed_doc["pickup_country"] = None

        # Get Pickup State
        try:
            transformed_doc["pickup_state"] = str(element["payload"]["tripDetails"]["pickupAddress"]["state"])
        except Exception:
            transformed_doc["pickup_state"] = None

        # Get Pickup State
        try:
            transformed_doc["pickup_county"] = str(element["payload"]["tripDetails"]["pickupAddress"]["county"])
        except Exception:
            transformed_doc["pickup_county"] = None

        # Get Pickup City
        try:
            transformed_doc["pickup_city"] = str(element["payload"]["tripDetails"]["pickupAddress"]["city"])
        except Exception:
            transformed_doc["pickup_city"] = None

        # Get Dropoff Start Date
        try:
            transformed_doc["dropoff_start_date"] = element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffStartDate']
        except Exception:
            transformed_doc["dropoff_start_date"] = None

        # Get Dropoff End Date
        try:
            transformed_doc["dropoff_end_date"] = element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffEndDate']
        except Exception:
            transformed_doc["dropoff_end_date"] = None

        # Get Dropoff Start Time
        try:
            dropoff_start_time = datetime.datetime.strptime(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffStartTime'], '%I:%M %p').time()
        except Exception:
            dropoff_start_time = None

        # Get Dropoff End Time
        try:
            dropoff_end_time = datetime.datetime.strptime(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffEndTime'], '%I:%M %p').time()
        except Exception:
            dropoff_end_time = None

        # Add time to dates
        if dropoff_start_time and transformed_doc["dropoff_start_date"]:

            try:
                transformed_doc["dropoff_start_date"] = transformed_doc["dropoff_start_date"].replace(
                    hour=dropoff_start_time.hour,
                    minute=dropoff_start_time.minute
                )

            # If error use date as a datetime
            except Exception:
                transformed_doc["dropoff_start_date"] = transformed_doc["dropoff_start_date"]

        try:
            transformed_doc["dropoff_start_date"] = transformed_doc["dropoff_start_date"].isoformat()
        except Exception:
            transformed_doc["dropoff_start_date"] = None

        # Add time to dates
        if dropoff_end_time and transformed_doc["dropoff_end_date"]:

            try:
                transformed_doc["dropoff_end_date"] = transformed_doc["dropoff_end_date"].replace(
                    hour=dropoff_end_time.hour,
                    minute=dropoff_end_time.minute
                )

            # If error use date as a datetime
            except Exception:
                pass

        try:
            transformed_doc["dropoff_end_date"] = transformed_doc["dropoff_end_date"].isoformat()
        except Exception:
            transformed_doc["dropoff_end_date"] = None

        # Get Dropoff Start Lat
        try:
            transformed_doc["dropoff_lat"] = float(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffCoordinates']['lat'])
        except Exception:
            transformed_doc["dropoff_lat"] = None

        # Get Dropoff Start Lon
        try:
            transformed_doc["dropoff_lon"] = float(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffCoordinates']['lng'])
        except Exception:
            transformed_doc["dropoff_lon"] = None

        # get Dropoff State
        try:
            transformed_doc["dropoff_country"] = str(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffAddress'][
                "country"])
        except Exception:
            transformed_doc["dropoff_country"] = None

        # Get Dropoff Country
        try:
            transformed_doc["dropoff_state"] = str(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffAddress'][
                "state"])
        except Exception:
            transformed_doc["dropoff_state"] = None

        # Get Dropoff County
        try:
            transformed_doc["dropoff_county"] = str(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffAddress'][
                "county"])
        except Exception:
            transformed_doc["dropoff_county"] = None

        # Get Dropoff City
        try:
            transformed_doc["dropoff_city"] = str(element["payload"]["tripDetails"]['dropoffs'][-1]['dropoffAddress'][
                "city"])
        except Exception:
            transformed_doc["dropoff_city"] = None

        # Get Per Mile Rate
        try:
            transformed_doc["per_mile_rate"] = float(element["payload"]["loadPay"]["perMileRate"])
        except Exception:
            transformed_doc["per_mile_rate"] = None

        # Get Price
        try:
            transformed_doc["price"] = float(element["payload"]["loadPay"]["amount"])
        except Exception:
            transformed_doc["price"] = None

        # Get Equipment Type List
        try:
            transformed_doc["equipment_type_list"] = str(', '.join(get_equipment_type_list(element)))
        except Exception as e:
            transformed_doc["equipment_type_list"] = None

        # Get FTL
        try:
            transformed_doc["ftl"] = bool(element["payload"]["loads"][0]["loadContentDetails"]["ftl"])
        except Exception:
            transformed_doc["ftl"] = None

        # Distance
        try:
            transformed_doc["distance"] = int(element["payload"]["tripDetails"]["distance"])
        except:
            transformed_doc["distance"] = None

        if transformed_doc["distance"] is None:
            try:
                transformed_doc["distance"] = int(element["account"]["distance"])
            except:
                transformed_doc["distance"] = None

        if transformed_doc["distance"] == 0:
            transformed_doc["distance"] = None

        # Customer Name
        try:
            transformed_doc["customer_name"] = str(element["payload"]["customerName"])
        except:
            transformed_doc["customer_name"] = None

        # Company Name
        try:
            transformed_doc["company_name"] = str(element["account"]["companyName"])
        except:
            transformed_doc["company_name"] = None

        # Commodity Description
        try:
            transformed_doc["commodity_description"] = str(element["payload"]["loads"][0]["loadContentDetails"]["commodityDescription"]["description"])
        except:
            transformed_doc["commodity_description"] = None

        # Special Care Instructions
        try:
            transformed_doc["special_care_instructions"] = str(element["payload"]["loads"][0]["loadContentDetails"]["commodityDescription"]["specialCareInstructions"])
        except:
            transformed_doc["special_care_instructions"] = None

        # Comment
        try:
            transformed_doc["comment"] = str(element["account"]["phone"])
        except:
            transformed_doc["comment"] = None

        # Contact Phone
        try:
            transformed_doc["contact_phone"] = str(element["account"]["contact_phone"])
        except:
            transformed_doc["contact_phone"] = None

        # Contact Email
        try:
            transformed_doc["contact_email"] = str(element["account"]["contactEmail"])
        except:
            transformed_doc["contact_email"] = None

        # MC
        try:
            transformed_doc["mc"] = str(element["account"]["mc"])
        except:
            transformed_doc["mc"] = None

        # DOT
        try:
            transformed_doc["dot"] = str(element["account"]["dot"])
        except:
            transformed_doc["dot"] = None

        # Assigned Date
        try:
            transformed_doc["assigned_date"] = element["payload"]["assignedDate"].isoformat()
        except:
            transformed_doc["assigned_date"] = None

        # Weight
        transformed_doc["weight"] = 0
        for load in element["payload"]["loads"]:
            try:
                weight = load["loadContentDetails"]["weight"]["amount"]
                transformed_doc["weight"] += int(weight)
            except:
                continue

        if transformed_doc["weight"] == 0:
            transformed_doc["weight"] = None

        cleaned_doc = {k: v if ((not isinstance(v, float) and not isinstance(v, int)) or float('-inf') < v < float('inf')) else None for k, v in transformed_doc.items()}

        return [cleaned_doc, ]


class TransformLoads(beam.PTransform):

    def expand(self, pcoll):
        from apache_beam import ParDo

        return pcoll | ParDo(_TransformLoads())
