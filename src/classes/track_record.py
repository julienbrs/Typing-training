import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDS_PATH = os.path.join(BASE_DIR, 'records.txt')

def is_float(value):
    """Verifies if a value can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def write_record_to_file(record):
    """ Writes records to a file """
    with open(RECORDS_PATH, 'a') as file:
        file.write('\n' + str(record))
    save_wpm_results()


def read_records_from_file():
    """Reads records from the file and returns a list of WPM results."""
    with open(RECORDS_PATH, 'r') as file:
        records = file.readlines()
    return [float(record.strip()) for record in records if is_float(record.strip())]


def save_wpm_results():
    wpm_results = read_records_from_file()

    trials = list(range(1, len(wpm_results) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(trials, wpm_results, marker='o',
             linestyle='-', color='b', markersize=8)

    plt.fill_between(trials, wpm_results, color="yellow",
                     alpha=0.1)  # Remplissage jaune poussin
    plt.title('Typing Test WPM Over Time',
              fontsize=18, fontweight='bold', color='darkblue')
    plt.xlabel('Trial Number', fontsize=14, color='darkblue')
    plt.ylabel('Words Per Minute (WPM)', fontsize=14, color='darkblue')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    plt.xticks(trials)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.savefig('wpm_results.png', format='png', dpi=300)

if __name__ == "__main__":
    save_wpm_results()
