from statistics import mean

class Institute:
    def __init__(self, name='', surname=''):
        self.name = name
        self.surname = surname
        self._status = 'Общий'
   
    def __str__(self):
        string = f"""{self._status}:
        Имя: {self.name}
        Фамилия: {self.surname}"""
        
        return string
    
    def __lt__(self, subject):
        if self.check_same_class(subject):
            return self.get_average_grade() < subject.get_average_grade()
        else:
            return None
    
    def __le__(self, subject):
        if self.check_same_class(subject):
            return self.get_average_grade() <= subject.get_average_grade()
        else:
            return None
   
    def __eq__(self, subject):
        if self.check_same_class(subject):
            return self.get_average_grade() == subject.get_average_grade()
        else:
            return None

    def __ne__(self, subject):
        if self.check_same_class(subject):
            return self.get_average_grade() != subject.get_average_grade()
        else:
            return None
        
    def _check_endstring_symbol(self, string, symbol, count):
        if string[-count:] == symbol:
            return True
        else:
            return False
            
    def _value_to_string(self, string, value, symbol=False, count=2):
        if len(string) > 0:
            if symbol == False:
                string += f", {value}"
            else:
                if symbol == '\n':
                    string += f"\n{value}"
                else:
                    if self._check_endstring_symbol(string, symbol, count):
                        string += f"{value}"
                    else:
                        string += f", {value}"  
        else:
            string = f"{value}"
            
        return string
    
    def _average_grade(self, subject):
        if subject == False:
            grade = [mean(val) for key, val in self.grades.items()]
            average = round(mean(grade), 3)
        else:
            if subject in self.grades:
                average = round(mean(self.grades[subject]), 3)
            else:
                average = False
        
        return average
            
    def _get_list_grade(self):
        string = ''
        symbol_for_title = '\n'
        for course, grade in self.grades.items():
            string = f"{self._value_to_string(string, course, symbol_for_title)}: "
            for g in grade:
                string = f"{self._value_to_string(string, g, ': ')}"
        
        return string
    
    def _list_courses(self, courses_list):
        courses = '' 
        for course in getattr(self, courses_list):
            courses = self._value_to_string(courses, course)
        
        return courses
    
    def _set_grade(self, subject, course, grade):
        if grade > 0 and grade <= 10:
            if course in subject.grades:
                subject.grades[course] += [grade]
            else:
                subject.grades[course] = [grade]
            return True
        else:
            return False
        
    def check_same_class(self, subject):
        if type(self).__name__ == type(subject).__name__:
            return True
        else:
            return False
        
    def get_average_grade(self, subject, course):
        if len(subject) > 0 and len(course) > 0:
            average = 0
            for sub in subject:
                average += sub._average_grade(course)
            return average
        else:
            return False
    
    def name_to_string(self):
        return f"{self.name} {self.surname}"

class Mentor(Institute):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self._status = 'Преподователь'
        self.courses_attached = []

class Student(Institute):    
    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        self._status = 'Студент'
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def __str__(self):
        average = self.get_average_grade()
        courses_progress = self.get_list_course('courses_in_progress')
        courses_finished = self.get_list_course('finished_courses')
        
        string = f"""{super().__str__()}
        Средняя оценка за домашние задания: {average}
        Курсы в процессе изучения: {courses_progress}
        Завершенные курсы: {courses_finished}"""
        
        return string
    
    def get_list_course(self, courses_list):
        return self._list_courses(courses_list)

    def get_grade(self):
        return self._get_list_grade()
        
    def get_average_grade(self, courses=False):
        return self._average_grade(courses)
     
    def set_grade(self, lector, course, grade):
        if isinstance(lector, Lector) and course in lector.courses_attached and course in self.courses_in_progress:
            return self._set_grade(lector, course, grade)
            #string = f"Ваша оценка '{grade}' вне 10 бальной шкалы оценок."
            #result = False
        else:
            return False
            #string = f"Курс '{course}' не закреплен за '{lector.name} {lector.surname}'."
            #result = False
    
class Lector(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self._status = 'Лектор'
        self.grades = {}

    def __str__(self):
        average = self.get_average_grade()
        string = f"""{super().__str__()}
        Средняя оценка за лекции: {average}""" 
        
        return string

    def get_average_grade(self, lectios=False):
        return self._average_grade(lectios)

    def get_grade(self):
        return self._get_list_grade()
    
    def set_grade(self):
        return False
        
class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self._status = 'Эксперт'
        
    def set_grade(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            return self._set_grade(student, course, grade)
            #string = f"Ваша оценка '{grade}' вне 10 бальной шкалы оценок."
            #print(string)
        else:
            return False
            #string = f"'{student.name} {student.surname}' не учится на курсе '{course}'."
            #print(string)

best_student = Student('Ruoy', 'Eman', 'men')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['Git']
best_student.courses_in_progress += ['Web']
best_student.finished_courses += ['SQL']

two_student = Student('Ryan', 'Reynolds', 'men')
two_student.courses_in_progress += ['Python']
two_student.courses_in_progress += ['Git']
two_student.courses_in_progress += ['Web']
two_student.finished_courses += ['SQL']

ed_lector = Lector('Edd', 'Stark')
ed_lector.courses_attached += ['Python']
ed_lector.courses_attached += ['Git']
ed_lector.courses_attached += ['Web']

jon_lector = Lector('Jon', 'Snow')
jon_lector.courses_attached += ['Python']
jon_lector.courses_attached += ['Git']
jon_lector.courses_attached += ['Web']

cool_mentor = Reviewer('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']
cool_mentor.courses_attached += ['Git']
cool_mentor.courses_attached += ['Web']

cool_mentor.set_grade(best_student, 'Python', 10)
cool_mentor.set_grade(best_student, 'Python', 9)
cool_mentor.set_grade(best_student, 'Python', 9)
cool_mentor.set_grade(best_student, 'Python', 10)
cool_mentor.set_grade(best_student, 'Git', 9)
cool_mentor.set_grade(best_student, 'Git', 10)
cool_mentor.set_grade(best_student, 'Web', 10)
cool_mentor.set_grade(best_student, 'Web', 7)
cool_mentor.set_grade(best_student, 'Web', 10)

cool_mentor.set_grade(two_student, 'Python', 10)
cool_mentor.set_grade(two_student, 'Python', 8)
cool_mentor.set_grade(two_student, 'Python', 9)
cool_mentor.set_grade(two_student, 'Python', 10)
cool_mentor.set_grade(two_student, 'Git', 9)
cool_mentor.set_grade(two_student, 'Git', 10)
cool_mentor.set_grade(two_student, 'Web', 10)
cool_mentor.set_grade(two_student, 'Web', 9)
cool_mentor.set_grade(two_student, 'Web', 10)

best_student.set_grade(ed_lector, 'Python', 10)
best_student.set_grade(ed_lector, 'Python', 10)
best_student.set_grade(ed_lector, 'Python', 10)
best_student.set_grade(ed_lector, 'Python', 9.9)
best_student.set_grade(ed_lector, 'Git', 10)
best_student.set_grade(ed_lector, 'Git', 10)
best_student.set_grade(ed_lector, 'Web', 8)
best_student.set_grade(ed_lector, 'Web', 9.9)
best_student.set_grade(ed_lector, 'Web', 10)

two_student.set_grade(jon_lector, 'Python', 10)
two_student.set_grade(jon_lector, 'Python', 8)
two_student.set_grade(jon_lector, 'Python', 9)
two_student.set_grade(jon_lector, 'Python', 10)
two_student.set_grade(jon_lector, 'Git', 8)
two_student.set_grade(jon_lector, 'Git', 10)
two_student.set_grade(jon_lector, 'Web', 10)
two_student.set_grade(jon_lector, 'Web', 9.9)
two_student.set_grade(jon_lector, 'Web', 10)


institut_grage = Institute()
student = [best_student, two_student]
lector = [ed_lector, jon_lector]
course = 'Python'
mess_student = f'Средняя оценка студентов на курсе "{course}"'
mess_lector = f'Средняя оценка преподавателей на курсе "{course}"'

print(f'{mess_student}: {institut_grage.get_average_grade(student, course)}')
print(f'{mess_lector}: {institut_grage.get_average_grade(lector, course)}')

print(f'Сравнение студентов "{two_student.name_to_string()} == {best_student.name_to_string()}" ==> {two_student == best_student}')
print(two_student)
print(best_student)

print(f'Сравнение преподавателей "{jon_lector.name_to_string()} < {ed_lector.name_to_string()}" ==> {jon_lector < ed_lector}')
print(jon_lector)
print(ed_lector)

print(f'Средняя оценка студента "{best_student.name_to_string()}": {best_student.get_average_grade()}')
print(f'Средняя оценка преподавателя "{ed_lector.name_to_string()}": {ed_lector.get_average_grade()}')

print(ed_lector.get_grade())
print(best_student.get_grade())