from llm_engine import call_llm
from prompts import tech_question_prompt
from utils import validate_email
from data_store import save_candidate


class ConversationManager:
    def __init__(self):
        self.stage = "greeting"
        self.data = {}

    def handle_message(self, user_input):

        # Greeting
        if self.stage == "greeting":
            self.stage = "name"
            return """👋 Welcome to TalentScout Hiring Assistant!

I will collect your basic details and then generate 
technical questions based on your tech stack.

Let's begin.

Please enter your Full Name."""

        # Name
        elif self.stage == "name":
            self.data["Full Name"] = user_input
            self.stage = "email"
            return "Please provide your Email Address."

        # Email validation
        elif self.stage == "email":
            if not validate_email(user_input):
                return "⚠ Please enter a valid email address."

            self.data["Email"] = user_input
            self.stage = "phone"
            return "Please provide your Phone Number."

        # Phone
        elif self.stage == "phone":
            self.data["Phone Number"] = user_input
            self.stage = "experience"
            return "How many years of experience do you have?"

        # Experience
        elif self.stage == "experience":
            self.data["Years of Experience"] = user_input
            self.stage = "position"
            return "What position are you applying for?"

        # Position
        elif self.stage == "position":
            self.data["Desired Position"] = user_input
            self.stage = "location"
            return "What is your current location?"

        # Location
        elif self.stage == "location":
            self.data["Current Location"] = user_input
            self.stage = "tech_stack"
            return "Please list your Tech Stack (languages, frameworks, tools). Separate by comma."

        # Tech Stack
        elif self.stage == "tech_stack":

            tech_list = [tech.strip() for tech in user_input.split(",")]
            self.data["Tech Stack"] = tech_list

            # Save candidate data locally
            save_candidate(self.data)

            questions = call_llm(
                "You are a strict senior technical interviewer.",
                tech_question_prompt(", ".join(tech_list)),
            )

            self.stage = "end"

            return (
                questions
                + "\n\nAfter answering these questions, type 'exit' to end the session."
            )

        # End
        elif self.stage == "end":
            return "✅ Thank you for your time! Our recruitment team will contact you shortly."
