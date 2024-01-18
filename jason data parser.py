import json



# Path to your JSON file
file_path = 'C:/Users/Shyamal/Desktop/daily use/data.txt'


# Read data from file
with open(file_path, 'r') as file:
    audit_log_data = json.load(file)

# Sample data - replace this with your actual audit log data
#audit_log_data = [...]  # Your JSON data here

# Filter and extract relevant information
file_activities = []
for entry in audit_log_data:
    if entry.get("ItemType") == "File":
        activity = {
            "Operation": entry.get("Operation"),
            "User": entry.get("UserId"),
            "Time": entry.get("CreationTime"),
            "FileName": entry.get("SourceFileName"),
            "ListId": entry.get("ListId"),
            "ObjectId": entry.get("ObjectId")
        }
        file_activities.append(activity)

# Print or process the filtered data
for activity in file_activities:
    print(activity)
