# ingest_edgar.py
import argparse

SAMPLE = '''Company: ExampleCorp
Date: 2023-11-01
Text: The company reported net income of $120 million for the quarter. Revenue increased 8% year-over-year driven by higher subscription sales. Management highlighted risk related to supply chain and currency headwinds.
---
Company: ExampleCorp
Date: 2023-08-01
Text: In the MD&A, management disclosed plans to invest $50 million in R&D and indicated expected margin expansion next year. EPS guidance was revised upward.
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='../sample_data/sample_edgar.txt')
    args = parser.parse_args()
    with open(args.out, 'w') as f:
        f.write(SAMPLE)
    print('Wrote sample to', args.out)
