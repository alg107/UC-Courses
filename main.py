import UCCourses

courses = [
        "PHYS310",
        "PHYS326",
        "MATH302",
        "MATH343",
        "PHYS311",
        "PHYS330",
        "MATH363",
        "MATH303",
        "PHYS313"
        ]

coursesS1 = [
        "MATH302",
        "MATH343",
        "PHYS310",
        "PHYS311",
        "PHYS326"
        ]

coursesS2 = [
        "PHYS313",
        "MATH303",
        "MATH363",
        "MATH380"
        ]

c_list = UCCourses.process_course_list(coursesS1)

timetable = UCCourses.gen_timetable(c_list)
print("Loaded.")

print("Visual Representation of Timetable:\n")

UCCourses.timetable_rep(timetable, True)


