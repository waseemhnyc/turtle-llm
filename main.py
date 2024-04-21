import instructor
import random
import turtle

from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

# wrap openai with instructor
client = instructor.from_openai(OpenAI())

# turtle setup
screen = turtle.Screen()
screen.setup(1.0, 1.0)
t = turtle.Turtle()


# turtle response models
class TurtleSteps(BaseModel):
	linear_val: int = Field(
		default=50,
		description="The value if the turtle is moving forward or backward."
	)
	angular_val: int = Field(
		default=90,
		description="The value if the turtle is turning left or right."
    )
	step_type: Literal["forward", "backward", "left", "right"]


class TurtlePrompter(BaseModel):
	steps: list[TurtleSteps] = Field(
		description="The steps for the turtle to take based on the instructions."
	)
	exit_loop: bool = Field(
		default=False,
		description="User request to stop or exit program."
	)


# main loop
while (True):
	user_input = input("Instruction: ")
	cur_position = t.position()

	response = client.chat.completions.create(
		model="gpt-4-turbo-preview",
		response_model=TurtlePrompter,
		messages=[
			{ 
				"role": "system", 
				"content": """
					You are tasked with moving a turtle. Take the current position 
					and the instructions and come up with the steps that turtle 
					should take.
					"""
			}, 
			{
				"role": "user",
				"content": f"""
					Current Position of Turtle: {cur_position}
					Instructions: {user_input}
				"""
			},
		],
	)

	t.color(random.choice(['blue', 'red', 'green', 'black']))

	for step in response.steps:
		if step.step_type == "forward":
			t.forward(step.linear_val)
		elif step.step_type == "backward":
			t.backward(step.linear_val)
		elif step.step_type == "left":
			t.left(step.angular_val)
		elif step.step_type == "right":
			t.right(step.angular_val)
		else:
			pass

	if response.exit_loop is True:
		break

print("Exited")
screen.mainloop()
