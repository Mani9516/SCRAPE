import ssl
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import streamlit as st
from openpyxl import Workbook
from datetime import datetime

# Function to scrape emails and phone numbers
def scrape_contacts(webpage):
    try:
        page = urlopen(webpage, context=ssl.SSLContext(ssl.PROTOCOL_TLS)) # Bypass SSL certificate verification
    except:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(webpage, headers=hdr)
        page = urlopen(req)

    scrape = BeautifulSoup(page, 'html.parser')
    scrape_text = scrape.get_text()

    phone_numbers = set(re.findall(r"((?:\d{3}|\(\d{3}\))?(?:\s|-|\.)?\d{3}(?:\s|-|\.)\d{4})", scrape_text))
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", scrape_text))

    return emails, phone_numbers

# Function to create personalized letter
def generate_personalized_letter(recipient_name, company_name, your_name, your_position, your_contact_info):
    letter_template = """
    Dear [Recipient's Name],

    I hope this email finds you well.

    I came across your contact information while researching [Company Name]. I was particularly impressed by [specific detail about the company].

    I wanted to reach out and introduce myself. My name is [Your Name] and I work at [Your Company]. We specialize in [Your Company's Products/Services] and have been helping businesses like yours [specific outcome or benefit].

    I would love the opportunity to discuss how we might be able to [solve a problem, provide value, etc.] for [Company Name].

    Please let me know if you would be interested in having a conversation. I am available for a call at your convenience.

    Looking forward to hearing from you.

    Best regards,
    [Your Name]
    [Your Position]
    [Your Contact Information]
    """

    personalized_letter = letter_template.replace("[Recipient's Name]", recipient_name)
    personalized_letter = personalized_letter.replace("[Company Name]", company_name)
    personalized_letter = personalized_letter.replace("[Your Name]", your_name)
    personalized_letter = personalized_letter.replace("[Your Position]", your_position)
    personalized_letter = personalized_letter.replace("[Your Contact Information]", your_contact_info)

    return personalized_letter

# Streamlit app
def main():
    st.title("SCRAPIFY")

    # Input fields
    webpage = st.text_input("Enter the webpage URL:")
    recipient_name = st.text_input("Enter the recipient's name:")
    company_name = st.text_input("Enter the recipient's company name:")
    your_name = st.text_input("Enter your name:")
    your_position = st.text_input("Enter your position:")
    your_contact_info = st.text_input("Enter your contact information:")

    # Button to trigger scraping and letter generation
    if st.button("Generate"):
        if webpage:
            # Scraping contacts
            emails, phone_numbers = scrape_contacts(webpage)

            # Display contacts
            if emails:
                st.write("Email addresses:")
                for email in emails:
                    st.write(email)
            else:
                st.write("No email addresses found.")

            if phone_numbers:
                st.write("Phone numbers:")
                for phone_number in phone_numbers:
                    st.write(phone_number)
            else:
                st.write("No phone numbers found.")

            # Generate personalized letter
            personalized_letter = generate_personalized_letter(recipient_name, company_name, your_name, your_position, your_contact_info)
            st.write("Personalized Letter:")
            st.write(personalized_letter)

if __name__ == "__main__":
    main()
