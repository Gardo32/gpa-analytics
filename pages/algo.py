import random


def final_exam_mark_estimation(start, finish, hour, mark):
    # Ensure valid range
    if start > finish:
        raise ValueError("Start should be less than or equal to finish.")

    # Calculate range size
    range_size = finish - start + 1

    # Calculate weights for each number in the range
    weights = []
    for i in range(start, finish + 1):
        # For higher hours, give more weight to lower numbers
        # For lower hours, give more weight to higher numbers
        weight = 1 / (abs(i - start) + 1) if hour > (finish - start) / 2 else 1 / (abs(finish - i) + 1)
        weights.append(weight)

    # Normalize weights
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]

    # Select a number based on the weighted distribution
    selected_number = random.choices(range(start, finish + 1), weights=normalized_weights, k=1)[0]
    selected_number = mark - selected_number
    return selected_number


def final_grade(grade, final, hour, type):
    if type == 'f4':
        result = ((grade / 100) * 60 + final) * hour
        return result
    elif type == 'f5':
        result = ((grade / 100) * 50 + final) * hour
        return result
    else:
        return 'Wrong Type'
