import numpy as np
import pandas as pd
import pickle
from google.cloud import bigquery
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder, LabelEncoder
from sklearn.preprocessing import PolynomialFeatures
from beam_utils.utils import upload_blob


def create_equipment_type_multilabel_binarizer():

    equipment_mlb = MultiLabelBinarizer()
    equipment_types = [
        "animalcarrier",
        "movingvan",
        "heavyhaulers",
        "boathauler",
        "container",
        "tanker",
        "auto",
        "stepdeck",
        "maxi",
        "doubledrop",
        "lowboy",
        "removeablegooseneck",
        "flatbed",
        "reefer",
        "landoll",
        "poweronly",
        "van",
        "hopperbottom",
        "dumptruck",
        "conestoga",
        "hazmat",
        ""]

    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    equipment_types
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        equipment_types.extend(str(row["equipment_types"]).split(", "))

    query = """
      SELECT DISTINCT 
      predicted_equipment_types
      FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
      """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        equipment_types.extend(str(row["predicted_equipment_types"]).split(", "))

    equipment_types = [i.upper().encode("utf-8") for i in equipment_types]
    equipment_mlb.fit([equipment_types])

    # Send Data to GCS Bucket
    pickle.dump(equipment_mlb, open("equipment_mlb.pkl", "wb"))
    upload_blob("load_transforms", "equipment_mlb.pkl", "load_equipment_mlb.pkl")
    upload_blob("user_transforms", "equipment_mlb.pkl", "user_equipment_mlb.pkl")

    return equipment_mlb


def create_quantile_multilabel_binarizer():

    load_quantile_mlb = MultiLabelBinarizer()
    quantiles = [
        "p0-p10",
        "p10-p25",
        "p25-p50",
        "p50-p75",
        "p75-p90",
        "p90-p100",
        ""]

    load_quantile_mlb.fit([quantiles])

    # Send Data to GCS Bucket
    pickle.dump(load_quantile_mlb, open("load_quantile_mlb.pkl", "wb"))
    upload_blob("load_transforms", "load_quantile_mlb.pkl", "load_quantile_mlb.pkl")

    return load_quantile_mlb


def create_one_hot_encoder_for_states():
    state_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    state_lbe = LabelEncoder()
    client = bigquery.Client()
    states = []

    query = """
         SELECT 
         DISTINCT
         UPPER(pickup_state) as state
         FROM
         `load-matching-ml-dev.feature_creation.loads_preprocessed`
         UNION ALL
         SELECT 
         DISTINCT
         UPPER(dropoff_state) as state
         FROM
         `load-matching-ml-dev.feature_creation.loads_preprocessed`
     """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        states.append(row["state"])

    query = """
            SELECT 
            DISTINCT
            UPPER(state) as state
            FROM
            `load-matching-ml-dev.feature_creation.users_preprocessed`
        """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        states.append(row["state"])

    query = """
            SELECT
            DISTINCT
            UPPER(operating_lanes_1_pickup_state) as state
            FROM
            `load-matching-ml-dev.feature_creation.users_preprocessed`
        """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        states.append(row["state"])

    query = """
              SELECT
              DISTINCT
              UPPER(common_lane_1_pickup_state) as state
              FROM
              `load-matching-ml-dev.feature_creation.users_preprocessed`
          """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        states.append(row["state"])

    states = state_lbe.fit_transform(states)
    state_ohe.fit(states.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(state_ohe, open("load_state_ohe.pkl", "wb"))
    upload_blob("load_transforms", "load_state_ohe.pkl", "load_state_ohe.pkl")
    upload_blob("user_transforms", "load_state_ohe.pkl", "user_state_ohe.pkl")
    pickle.dump(state_lbe, open("load_state_lbe.pkl", "wb"))
    upload_blob("load_transforms", "load_state_lbe.pkl", "load_state_lbe.pkl")
    upload_blob("user_transforms", "load_state_lbe.pkl", "user_state_lbe.pkl")
    return (state_lbe, state_ohe)


def create_one_hot_encoder_for_cities():

    city_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    city_lbe = LabelEncoder()
    client = bigquery.Client()
    state_cities = []

    query = """
        SELECT 
        DISTINCT
        UPPER(pickup_city) as city
        FROM
        `load-matching-ml-dev.feature_creation.loads_preprocessed`
        UNION ALL
        SELECT 
        DISTINCT
        UPPER(dropoff_city) as city
        FROM
        `load-matching-ml-dev.feature_creation.loads_preprocessed`
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT 
           DISTINCT
           UPPER(city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_1_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_2_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_3_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_4_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_5_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_1_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_2_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_3_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_4_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(operating_lanes_5_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_1_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_2_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_3_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_4_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_5_pickup_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_1_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_2_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_3_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_4_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    query = """
           SELECT
           DISTINCT
           UPPER(common_lane_5_dropoff_city) as city
           FROM
           `load-matching-ml-dev.feature_creation.users_preprocessed`
       """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    for row in rows:
        state_cities.append(row["city"])

    state_cities = city_lbe.fit_transform(state_cities)
    city_ohe.fit(state_cities.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(city_ohe, open("load_city_ohe.pkl", "wb"))
    upload_blob("load_transforms", "load_city_ohe.pkl", "load_city_ohe.pkl")
    upload_blob("user_transforms", "load_city_ohe.pkl", "user_city_ohe.pkl")
    pickle.dump(city_lbe, open("load_city_lbe.pkl", "wb"))
    upload_blob("load_transforms", "load_city_lbe.pkl", "load_city_lbe.pkl")
    upload_blob("user_transforms", "load_city_lbe.pkl", "user_city_lbe.pkl")
    return (city_lbe, city_ohe)


def create_one_hot_encoder_load_source():
    source_ohe = OneHotEncoder(handle_unknown='ignore')
    source_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    source
    FROM `load-matching-ml-dev.feature_creation.loads_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    sources = []

    for row in rows:
        sources.append(row["source"])

    sources = source_lbe.fit_transform(sources)
    source_ohe.fit(sources.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(source_ohe, open("load_source_ohe.pkl", "wb"))
    upload_blob("load_transforms", "load_source_ohe.pkl", "load_source_ohe.pkl")
    pickle.dump(source_lbe, open("load_source_lbe.pkl", "wb"))
    upload_blob("load_transforms", "load_source_lbe.pkl", "load_source_lbe.pkl")
    return (source_lbe, source_ohe)


def create_one_hot_encoder_email():

    email_ohe = OneHotEncoder(handle_unknown='ignore')
    email_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    contact_email
    FROM `load-matching-ml-dev.feature_creation.loads_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    emails = []

    for row in rows:
        emails.append(row["contact_email"])

    emails = email_lbe.fit_transform(emails)
    email_ohe.fit(emails.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(email_ohe, open("load_email_ohe.pkl", "wb"))
    upload_blob("load_transforms", "load_email_ohe.pkl", "load_email_ohe.pkl")
    pickle.dump(email_lbe, open("load_email_lbe.pkl", "wb"))
    upload_blob("load_transforms", "load_email_lbe.pkl", "load_email_lbe.pkl")
    return (email_lbe, email_ohe)


def get_load_quantiles():

    client = bigquery.Client()

    query = """
    SELECT 
    * 
    FROM `load-matching-ml-dev.feature_creation.load_quantile_features` 
    WHERE p10 is not null
    """
    df = client.query(query).to_dataframe()
    return df


def map_quantiles_for_entry(feature_name, input_df, row):

    mapping = []

    # Get Feature Quantiles for Load
    load_feature = row[feature_name]
    if str(load_feature).lower() == "nan":
        mapping.append("")
    else:
        feature_df = input_df[input_df['feature_name'] == (feature_name + "_quantiles")]

        # Check if in p0-p25 quadrant
        if load_feature < feature_df.iloc[0]["p10"]:
            mapping.append("p0-p10")

        # Check if in p10-p25 quadrant
        if load_feature >= feature_df.iloc[0]["p10"]:
            if load_feature < feature_df.iloc[0]["p25"]:
                mapping.append("p10-p25")
            elif feature_df.iloc[0]["p10"] == feature_df.iloc[0]["p75"] and load_feature < feature_df.iloc[0]["p90"]:
                mapping.append("p10-p25")
            elif feature_df.iloc[0]["p10"] == feature_df.iloc[0]["p50"] and load_feature < feature_df.iloc[0]["p75"]:
                mapping.append("p10-p25")
            elif feature_df.iloc[0]["p10"] == feature_df.iloc[0]["p25"] and load_feature < feature_df.iloc[0]["p50"]:
                mapping.append("p10-p25")

        # Check if in p25-p50 quadrant
        if load_feature >= feature_df.iloc[0]["p25"]:
            if load_feature < feature_df.iloc[0]["p50"]:
                mapping.append("p25-p50")
            elif feature_df.iloc[0]["p25"] == feature_df.iloc[0]["p75"] and load_feature < feature_df.iloc[0]["p90"]:
                mapping.append("p25-p50")
            elif feature_df.iloc[0]["p25"] == feature_df.iloc[0]["p50"] and load_feature < feature_df.iloc[0]["p75"]:
                mapping.append("p25-p50")

        # Check if in p50-p75 quadrant
        if load_feature >= feature_df.iloc[0]["p50"]:
            if load_feature < feature_df.iloc[0]["p75"]:
                mapping.append("p50-p75")
            elif feature_df.iloc[0]["p50"] == feature_df.iloc[0]["p75"] and load_feature < feature_df.iloc[0]["p90"]:
                mapping.append("p50-p75")

        # Check if in p75-p90 quadrant
        if feature_df.iloc[0]["p75"] <= load_feature < feature_df.iloc[0]["p90"]:
            mapping.append("p75-p90")

        # Check if in p90-p100 quadrant
        if load_feature >= feature_df.iloc[0]["p90"]:
            mapping.append("p90-p100")

    return mapping


def get_p50_value(feature_name, quantile_df):
    feature_df = quantile_df[quantile_df['feature_name'] == (feature_name + "_quantiles")]
    return feature_df.iloc[0]["p50"]


def create_time_features(feature_name_list, input_df):

    for feature in feature_name_list:
        if "hour" in feature:
            conversion = 24
        elif "day_of_week" in feature:
            conversion = 7
        elif "month" in feature:
            conversion = 12
        elif "day_of_year" in feature:
            conversion = 365

        input_df[feature].fillna(value=pd.np.nan, inplace=True)
        input_df['sin_' + feature] = np.sin(2 * np.pi * input_df[feature] / conversion)
        input_df['cos_' + feature] = np.cos(2 * np.pi * input_df[feature] / conversion)
        input_df.drop(feature, axis=1, inplace=True)

    return input_df


def create_polynomial_features(feature_name_list, input_df):

    df = input_df[feature_name_list]
    pf = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
    res = pf.fit_transform(df)
    poly_features = pd.DataFrame(res)
    output_df = pd.concat([input_df, poly_features], axis=1)

    return output_df


def create_one_hot_encoder_for_user_zip_code():
    zip_code_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    zip_code_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT zip_code
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    zip_codes = []
    for row in rows:
        zip_codes.append(row["zip_code"])

    zip_codes = zip_code_lbe.fit_transform(zip_codes)
    zip_code_ohe.fit(zip_codes.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(zip_code_ohe, open("user_zip_code_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_zip_code_ohe.pkl", "user_zip_code_ohe.pkl")
    pickle.dump(zip_code_lbe, open("user_zip_code_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_zip_code_lbe.pkl", "user_zip_code_lbe.pkl")
    return (zip_code_lbe, zip_code_ohe)


def create_one_hot_encoder_for_user_zip_code():
    zip_code_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    zip_code_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT zip_code
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    zip_codes = []
    for row in rows:
        zip_codes.append(row["zip_code"])

    zip_codes = zip_code_lbe.fit_transform(zip_codes)
    zip_code_ohe.fit(zip_codes.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(zip_code_ohe, open("user_zip_code_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_zip_code_ohe.pkl", "user_zip_code_ohe.pkl")
    pickle.dump(zip_code_lbe, open("user_zip_code_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_zip_code_lbe.pkl", "user_zip_code_lbe.pkl")
    return (zip_code_lbe, zip_code_ohe)


def create_one_hot_encoder_for_user_dot():
    dot_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    dot_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT dot
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    dots = []
    for row in rows:
        dots.append(row["dot"])

    dots = dot_lbe.fit_transform(dots)
    dot_ohe.fit(dots.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(dot_ohe, open("user_dot_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_dot_ohe.pkl", "user_dot_ohe.pkl")
    pickle.dump(dot_lbe, open("user_dot_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_dot_lbe.pkl", "user_dot_lbe.pkl")
    return (dot_lbe, dot_ohe)


def create_one_hot_encoder_for_user_email():
    email_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    email_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    email
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    emails = []
    for row in rows:
        emails.append(row["email"])

    emails = email_lbe.fit_transform(emails)
    email_ohe.fit(emails.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(email_ohe, open("user_email_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_email_ohe.pkl", "user_email_ohe.pkl")
    pickle.dump(email_lbe, open("user_email_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_email_lbe.pkl", "user_email_lbe.pkl")
    return (email_lbe, email_ohe)


def create_one_hot_encoder_for_user_hos_cycle():
    hos_cycle_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    hos_cycle_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    hos_cycle
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    hos_cycles = []
    for row in rows:
        hos_cycles.append(row["hos_cycle"])

    hos_cycles = hos_cycle_lbe.fit_transform(hos_cycles)
    hos_cycle_ohe.fit(hos_cycles.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(hos_cycle_ohe, open("user_hos_cycle_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_hos_cycle_ohe.pkl", "user_hos_cycle_ohe.pkl")
    pickle.dump(hos_cycle_lbe, open("user_hos_cycle_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_hos_cycle_lbe.pkl", "user_hos_cycle_lbe.pkl")
    return (hos_cycle_lbe, hos_cycle_ohe)


def create_one_hot_encoder_for_user_hos_home_timezone():
    hos_home_timezone_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    hos_home_timezone_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    hos_home_timezone
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    hos_home_timezones = []
    for row in rows:
        hos_home_timezones.append(row["hos_home_timezone"])

    hos_home_timezones = hos_home_timezone_lbe.fit_transform(hos_home_timezones)
    hos_home_timezone_ohe.fit(hos_home_timezones.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(hos_home_timezone_ohe, open("user_hos_home_timezone_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_hos_home_timezone_ohe.pkl", "user_hos_home_timezone_ohe.pkl")
    pickle.dump(hos_home_timezone_lbe, open("user_hos_home_timezone_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_hos_home_timezone_lbe.pkl", "user_hos_home_timezone_lbe.pkl")
    return (hos_home_timezone_lbe, hos_home_timezone_ohe)


def create_one_hot_encoder_for_user_type():
    user_type_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    user_type_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    user_type
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    user_types = []
    for row in rows:
        user_types.append(row["user_type"])

    user_types = user_type_lbe.fit_transform(user_types)
    user_type_ohe.fit(user_types.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(user_type_ohe, open("user_type_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_type_ohe.pkl", "user_type_ohe.pkl")
    pickle.dump(user_type_lbe, open("user_type_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_type_lbe.pkl", "user_type_lbe.pkl")
    return (user_type_lbe, user_type_ohe)


def create_one_hot_encoder_for_user_mc_number():
    mc_number_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    mc_number_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    mc_number
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    mc_numbers = []
    for row in rows:
        mc_numbers.append(row["mc_number"])

    mc_numbers = mc_number_lbe.fit_transform(mc_numbers)
    mc_number_ohe.fit(mc_numbers.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(mc_number_ohe, open("user_mc_number_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_mc_number_ohe.pkl", "user_mc_number_ohe.pkl")
    pickle.dump(mc_number_lbe, open("user_mc_number_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_mc_number_lbe.pkl", "user_mc_number_lbe.pkl")
    return (mc_number_lbe, mc_number_ohe)


def create_one_hot_encoder_for_user_channel():
    channel_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    channel_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    channel
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    channels = []
    for row in rows:
        channels.append(row["channel"])

    channels = channel_lbe.fit_transform(channels)
    channel_ohe.fit(channels.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(channel_ohe, open("user_channel_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_channel_ohe.pkl", "user_channel_ohe.pkl")
    pickle.dump(channel_lbe, open("user_channel_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_channel_lbe.pkl", "user_channel_lbe.pkl")
    return (channel_lbe, channel_ohe)


def create_one_hot_encoder_for_safer_safety_rating():
    safer_result_safety_rating_ohe = OneHotEncoder(handle_unknown='ignore', sparse=True)
    safer_result_safety_rating_lbe = LabelEncoder()
    client = bigquery.Client()

    query = """
    SELECT DISTINCT 
    safer_result_safety_rating
    FROM `load-matching-ml-dev.feature_creation.users_preprocessed` 
    """

    query_job = client.query(query)  # API request
    rows = query_job.result()

    ratings = []
    for row in rows:
        ratings.append(row["safer_result_safety_rating"])

    safer_result_safety_ratings = safer_result_safety_rating_lbe.fit_transform(ratings)
    safer_result_safety_rating_ohe.fit(safer_result_safety_ratings.reshape(-1, 1))

    # Send Data to GCS Bucket
    pickle.dump(safer_result_safety_rating_ohe, open("user_safer_result_safety_rating_ohe.pkl", "wb"))
    upload_blob("user_transforms", "user_safer_result_safety_rating_ohe.pkl", "user_safer_result_safety_rating_ohe.pkl")
    pickle.dump(safer_result_safety_rating_lbe, open("user_safer_result_safety_rating_lbe.pkl", "wb"))
    upload_blob("user_transforms", "user_safer_result_safety_rating_lbe.pkl", "user_safer_result_safety_rating_lbe.pkl")
    return (safer_result_safety_rating_lbe, safer_result_safety_rating_ohe)
