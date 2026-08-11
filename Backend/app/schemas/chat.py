# from pydantic import BaseModel

# #Defines the schema for incoming data sent by the frontend client 
# #(e.g., your React/Vite app running on localhost:5173).
# class ChatRequest(BaseModel):      
#     session_id: str
#     message: str     # Forces the request body to contain a key named message holding a text string.

# #Defines the schema for outgoing data sent from your server back to the user.
# class ChatResponse(BaseModel):
#     session_id: str
#     response: str    #Guarantees the server replies with a uniform JSON object containing a response string.

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    problem_id: str
    message: str

    # Current contents of Monaco
    code: str = ""

    # Result from the most recent /api/run call
    execution_output: str = ""
    execution_error: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    response: str