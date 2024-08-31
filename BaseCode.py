numSubject = int(input("Enter the number of subjects: "))
hours = []
total = []

for i in range(numSubject):
    marks = int(input(f"Enter the marks of subject {i+1}: "))
    hour = int(input(f"Enter the hours of subject {i+1}: "))
    total.append(marks * hour)
    hours.append(hour)

total = sum(total)
hours = sum(hours)
final = total / hours

print(f"Your GPA is: {final}")
