# from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS
# import pyodbc

# app = Flask(__name__)
# # CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"]}})
# # CORS(app)

# # Define the database connection string
# connection_string = (
#     "Driver={ODBC Driver 18 for SQL Server};"
#     "Server=tcp:dbmsproject1.database.windows.net,1433;"
#     "Database=DBMSProject;"
#     "Uid=CloudSA07af89fd;"
#     "Pwd=DBMSproject123;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )

# @app.route('/')
# def hello():
#     return 'Welcome to Healthcare Management Application'

# @app.route('/api/insert-data', methods=['POST','OPTIONS'])
# def insert_data():
#     if request.method == 'OPTIONS':
#         # Manually set the CORS headers
#         response = make_response()
#         response.headers.set('Access-Control-Allow-Origin', '*')
#         response.headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS')
#         response.headers.set('Access-Control-Allow-Headers', 'Content-Type')
#         return response
#     if not request.is_json:
#         return jsonify({'error': 'Request must be JSON'}), 415
#     data = request.json.get('data')
#     print(data)
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400

#     try:
#         data = request.json['data']
#         table_name = data.pop('group')  # Extract and remove 'group' from data
#         print(data)

#         # Enclose column names in square brackets to handle reserved keywords
#         columns = ', '.join([f'[{key}]' for key in data.keys()])
#         placeholders = ', '.join(['?'] * len(data))
#         dynamic_insert_query = f"INSERT INTO dbo.{table_name} ({columns}) VALUES ({placeholders})"

#         # Establish a connection to the database
#         conn = pyodbc.connect(connection_string)
#         cursor = conn.cursor()

#         # Execute the dynamic insert query
#         cursor.execute(dynamic_insert_query, list(data.values()))
#         conn.commit()

#         return jsonify({'message': 'Data inserted successfully'}), 201
#     except Exception as e:
#         print(f"Error: {e}")  # Log the error for debugging
#         return jsonify({'error': str(e)}), 500
#     finally:
#         # Ensure the connection is closed
#         if 'conn' in locals() or 'conn' in globals():
#             conn.close()

# @app.route('/api/delete-entry', methods=['DELETE', 'OPTIONS'])
# def delete_entry():
#     if request.method == 'OPTIONS':
#         response = make_response()
#         response.headers.set('Access-Control-Allow-Origin', '*')
#         response.headers.set('Access-Control-Allow-Methods', 'DELETE, OPTIONS')
#         response.headers.set('Access-Control-Allow-Headers', 'Content-Type')
#         return response

#     data = request.json.get('data')

#     try:
#         # SQL query
#         conn = pyodbc.connect(connection_string)
#         cursor = conn.cursor()

#         data = request.json['data']
#         table_name = data.pop('group')
#         column_name = data.pop('columnName')
#         column_value = data.pop('columnValue') 

#         delete_query = f"DELETE FROM dbo.{table_name} WHERE {column_name} = ?"
#         print(delete_query)
#         cursor.execute(delete_query,column_value)

#         conn.commit()

#         return jsonify({'message': 'Entry deleted successfully'}), 200
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({'error': str(e)}), 500
#     finally:
#         if conn:
#             conn.close()


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
# CORS(app)  # Enable CORS for all domains on all routes
CORS(app, support_credentials=True)

# Define the database connection string
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:dbmsproject1.database.windows.net,1433;"
    "Database=DBMSProject;"
    "Uid=CloudSA07af89fd;"
    "Pwd=DBMSproject123;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

number_of_rows = 1000

@app.route('/')
def hello():
    return 'Welcome to Healthcare Management Application'

@app.route('/api/insert-data', methods=['POST', 'OPTIONS'])
def insert_data():
    if request.method == 'OPTIONS':
        # Automatically handled by flask-cors
        return {}

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415

    data1 = request.json.get('data')
    app.logger.info(f"Received data: {data1}")
    if not data1:
        return jsonify({'error': 'No data provided'}), 400

    try:
        data1 = request.json['data']
        table_name = data1.pop('group')  # Extract and remove 'group' from data
        app.logger.info(f"Processed data: {data1}")

        # Enclose column names in square brackets to handle reserved keywords
        columns = ', '.join([f'[{key}]' for key in data1.keys()])
        placeholders = ', '.join(['?'] * len(data1))
        dynamic_insert_query = f"INSERT INTO dbo.{table_name} ({columns}) VALUES ({placeholders})"

        # Establish a connection to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute the dynamic insert query
        cursor.execute(dynamic_insert_query, list(data1.values()))
        conn.commit()

        return jsonify({'message': 'Data inserted successfully'}), 201
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

@app.route('/api/delete-entry', methods=['DELETE', 'OPTIONS'])
def delete_entry():
    if request.method == 'OPTIONS':
        # Automatically handled by flask-cors
        return {}

    try:
        data = request.json.get('data')
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # SQL query
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        data = request.json['data']
        table_name = data.pop('group')
        column_name = data.pop('columnName')
        column_value = data.pop('columnValue')

        delete_query = f"DELETE FROM dbo.{table_name} WHERE {column_name} = ?"
        app.logger.info(delete_query)
        cursor.execute(delete_query, column_value)

        conn.commit()

        return jsonify({'message': 'Entry deleted successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/get-appointment', methods=['GET'])
def get_appointments():
    try:
        query = f"SELECT TOP {number_of_rows} AppointmentID,PatientID,MedicalProfessionalID,Status FROM dbo.appointment"
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        appointment_list = []
        for row in data:
            appointment_dict = {
                'AppointmentID': row.AppointmentID,
                'PatientID': row.PatientID,
                'MedicalProfessionalID': row.MedicalProfessionalID,
                'Status': row.Status
            }
            appointment_list.append(appointment_dict)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        data = []
    finally:
        conn.close()

    return jsonify(appointment_list), 200


@app.route('/api/get-patient', methods=['GET'])
def get_patients():
    try:
        query = f"SELECT TOP {number_of_rows} * FROM dbo.patient"
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        patient_list = []
        for row in data:
            patient_dict = {
                'PatientID': row.PatientID,
                'Name': row.Name,
                'Address': row.Address,
                'ContactNumber': row.ContactNumber,
                'Age': row.Age,
                'Gender': row.Gender,
                'BloodType': row.BloodType,
                'InsuranceID': row.InsuranceID,
                'EmergencyContact': row.EmergencyContact,
                'HospitalID': row.HospitalID,
                'MedicalCondition': row.MedicalCondition,
            }
            patient_list.append(patient_dict)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        data = []
    finally:
        conn.close()

    return jsonify(patient_list), 200

@app.route('/api/get-doctor', methods=['GET'])
def get_doctor():
    try:
        query = f"SELECT TOP {number_of_rows} * FROM dbo.MedicalProfessional"
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        doctor_list = []
        for row in data:
            doctor_dict = {
                'ProfessionalID': row.ProfessionalID,
                'Name': row.Name,
                'ContactNumber': row.ContactNumber,
                'Specialization': row.Specialization,
                'MedicalLicense': row.MedicalLicense,
            }
            doctor_list.append(doctor_dict)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        data = []
    finally:
        conn.close()

    return jsonify(doctor_list), 200

@app.route('/api/doctor-count', methods = ['GET'])
def doctor_count():
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        count = "Select COUNT(*) FROM [dbo].[MedicalProfessional]"
        cursor.execute(count)
        count = cursor.fetchone()[0]
        conn.close()
        return jsonify(count=count)

@app.route('/api/patient-count', methods = ['GET'])
def patient_count():
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        count = "SELECT COUNT(*) FROM dbo.Patient"
        cursor.execute(count)
        count = cursor.fetchone()[0]
        conn.close()
        return jsonify(count=count)


if __name__ == '__main__':
    app.run(debug=True)