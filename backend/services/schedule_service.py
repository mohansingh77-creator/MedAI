def generate_today_plan(medicines):

    plan = {}

    for medicine in medicines:

        timings = medicine.get("timing", [])

        # Backward compatibility
        if isinstance(timings, str):
            timings = [timings]

        for timing in timings:

            if timing not in plan:
                plan[timing] = []

            item = {
                "name": medicine["name"],
                "dosage": medicine["dosage"]
            }

            # Show frequency only for SOS / PRN medicines
            if medicine.get("frequency") == "When Required":
                item["frequency"] = "SOS"

            plan[timing].append(item)

    ordered_plan = []

    display_order = [

        "Morning",

        "Before Breakfast",

        "After Breakfast",

        "Before Lunch",

        "After Lunch",

        "Before Dinner",

        "After Dinner",

        "Night"

    ]

    for time in display_order:

        if time in plan:

            ordered_plan.append({

                "time": time,

                "medicines": plan[time]

            })

    return ordered_plan