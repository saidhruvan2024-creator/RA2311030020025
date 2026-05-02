import requests
import heapq
from datetime import datetime

API_URL = "http://20.207.122.201/evaluation-service/notifications"

# Priority weights
TYPE_WEIGHT = {
    "Placement": 100,
    "Result": 70,
    "Event": 40
}

TOP_N = 10


def calculate_priority(notification):
    """
    Calculates combined priority score using:
    weight + recency
    """

    notif_type = notification["Type"]
    timestamp = notification["Timestamp"]

    weight = TYPE_WEIGHT.get(notif_type, 0)

    # Convert timestamp into epoch seconds
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    epoch_time = dt.timestamp()

    # Final score
    return weight + epoch_time


def fetch_notifications():

    headers = {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
    }

    response = requests.get(
        API_URL,
        headers=headers
    )

    if response.status_code != 200:
        print("Response:", response.text)
        raise Exception(
            f"API Error: {response.status_code}"
        )

    data = response.json()

    return data.get("notifications", [])


def get_top_notifications(notifications):
    """
    Maintains top 10 notifications efficiently using min heap
    """

    min_heap = []

    for notification in notifications:

        score = calculate_priority(notification)

        heap_item = (
            score,
            notification
        )

        if len(min_heap) < TOP_N:
            heapq.heappush(min_heap, heap_item)

        else:
            if score > min_heap[0][0]:
                heapq.heapreplace(min_heap, heap_item)

    # Highest priority first
    result = sorted(
        min_heap,
        key=lambda x: x[0],
        reverse=True
    )

    return [item[1] for item in result]


def display_notifications(notifications):

    print("\n===== TOP 10 PRIORITY NOTIFICATIONS =====\n")

    for idx, notif in enumerate(notifications, start=1):

        print(f"{idx}. [{notif['Type']}]")
        print(f"   Message   : {notif['Message']}")
        print(f"   Timestamp : {notif['Timestamp']}")
        print(f"   ID        : {notif['ID']}")
        print()


if __name__ == "__main__":

    notifications = fetch_notifications()

    top_notifications = get_top_notifications(
        notifications
    )

    display_notifications(top_notifications)
