from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)
    competition = {
        "name": "Competition Test 1",
        "date": "2023-10-22 13:30:00",
        "numberOfPlaces": "50"
    }

    club = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }

    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", data={'email': self.club['email']})

    @task
    def get_booking(self):
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}")

    @task
    def post_booking(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club["name"],
                "competition": self.competition["name"],
                "places": 1,
            })

    @task
    def get_board(self):
        self.client.get("/pointsDisplay")
