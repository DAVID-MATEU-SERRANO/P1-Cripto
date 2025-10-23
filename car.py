class Car:
    def __init__(self, name: str, brand: str, owner: str, speed: int, handling: int, acceleration: int, braking: int):
        """Initializes a car with base stats."""
        self.name = name
        self.brand = brand
        self.owner = owner
        self.speed = speed
        self.handling = handling
        self.acceleration = acceleration
        self.braking = braking
        self.upgrades = []

    def add_turbo(self):
        """Adds a turbocharger, increasing top speed and acceleration."""
        self.speed += 2
        self.acceleration += 3
        self.upgrades.append("Turbocharger")

    def add_semislicks(self):
        """Installs semi-slick tires, improving handling but reducing top speed slightly."""
        self.handling += 3
        self.speed -= 1
        self.upgrades.append("Semi-slick Tires")

    def add_suspension(self):
        """Upgrades to a sport suspension system, improving handling and stability."""
        self.handling += 3
        self.upgrades.append("Sport Suspension")

    def add_rollcage(self):
        """Installs a roll cage, improving handling but slightly reducing acceleration."""
        self.handling += 2
        self.acceleration -= 1
        self.upgrades.append("Roll Cage")

    def add_ecu_remap(self):
        """Performs an ECU remap, improving speed and acceleration but reducing braking slightly."""
        self.speed += 1
        self.acceleration += 1
        self.braking -= 1
        self.upgrades.append("ECU Remap")

    def add_air_filter(self):
        """Adds a performance air filter, slightly improving acceleration but reducing top speed."""
        self.acceleration += 1
        self.speed -= 1
        self.upgrades.append("Performance Air Filter")

    def add_brakes(self):
        """Upgrades to performance brakes, improving braking efficiency."""
        self.braking += 3
        self.upgrades.append("Upgraded Brakes")

    def __str__(self):
        return (f"{self.brand} {self.name} owned by {self.owner} with upgrades: {', '.join(self.upgrades)}\n")# car.py