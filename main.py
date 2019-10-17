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
        "PHYS310",
        "PHYS326",
        "MATH302",
        "MATH343",
        "PHYS311"
        ]

coursesS2 = [
        "PHYS203",
        "PHYS206",
        "MATH202",
        "MATH240",
        "MATH365"
        ]

c_list = UCCourses.process_course_list(coursesS1)

timetable = UCCourses.gen_timetable(c_list)
print("Loaded.")

print("Visual Representation of Timetable:\n")

UCCourses.timetable_rep(timetable, True)
