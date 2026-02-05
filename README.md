# biomedical-phrase-extraction


## What this project does

- Queries PubMed using the NCBI Entrez API
- Retrieves article titles and abstracts
- Finds constructions involving a target disease term
- Extracts configurable context windows around those constructions

## NCBI account and email requirement

This project uses the NCBI Entrez API, which requires users to identify
themselves with an email address.

### Step 1. Sign up for NCBI

Create an NCBI account at:

https://www.ncbi.nlm.nih.gov/

### Step 2. Add your email to an environment file

Create a file named .env in the project root:

```ENTREZ_EMAIL=your_email@example.com```


This file should not be committed to GitHub. Make sure `.env` is listed in `.gitignore`.
