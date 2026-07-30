import csv
import io

def generate_evaluation_report(evaluations):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Bidder', 'Criteria', 'Score', 'Max Score', 'Passed', 'Comments'])
    for e in evaluations:
        writer.writerow([e.submission.bidder.company_name if e.submission and e.submission.bidder else '',
                        e.criteria_name, e.score, e.max_score, e.passed, e.comments])
    output.seek(0)
    return output
