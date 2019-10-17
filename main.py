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

c_list = UCCourses.process_course_list(courses)
for c in c_list:
    print(c.title)
