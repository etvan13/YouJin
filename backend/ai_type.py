import os
import importlib.util

class AI_Type:
    
    ####### UTILITIES #######
    
    def __init__(self):
        """Initialize paths and available AI methods."""
        # Paths to run_model.py in various directories
        self.lm_studio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_methods', 'lm_studio', 'run_model.py')
        self.local_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ai_methods', 'local_ai', 'run_model.py')
        
        # Dictionary to store available AI methods
        self.ai_methods = {}
        # Check which AI methods are available on initialization
        self.check_available_ais()

    def check_available_ais(self):
        """Check which AI methods are available by calling each check function."""
        if self.check_lm_studio():
            self.ai_methods['lm_studio'] = self.run_lm_studio
            print("LM Studio is available and added to ai_methods.")
        else:
            print("LM Studio is not available.")
        
        if self.check_local_model():
            self.ai_methods['local_model'] = self.run_local_model
            print("Local AI model is available and added to ai_methods.")
        else:
            print("Local AI model is not available.")

        # Fallback is always available
        self.ai_methods['user_input'] = self.run_user_input
        print("Fallback user input method added to ai_methods.")

    def get_available_ais(self):
        """Return a list of available AI methods."""
        return list(self.ai_methods.keys())

    def run_selected_ai(self, selected_ai, user_message):
        """Run the selected AI method based on user choice."""
        print(f"run_selected_ai called with selected_ai: {selected_ai}")
        print(f"Available AI methods: {list(self.ai_methods.keys())}")
        
        if selected_ai in self.ai_methods:
            print(f"Executing AI method: {selected_ai}")
            return self.ai_methods[selected_ai](user_message)
        else:
            print(f"Selected AI '{selected_ai}' is not available. Using fallback.")
            return self.run_user_input(user_message)
    
    ######## END UTILITIES #######


    ####### LM STUDIO ########

    def check_lm_studio(self):
        """Check if LM Studio AI model is available and the server is running."""
        if os.path.exists(self.lm_studio_path):
            try:
                # Load the run_model.py module dynamically
                spec = importlib.util.spec_from_file_location("run_model", self.lm_studio_path)
                run_model = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(run_model)

                # Call the 'check' function from run_model
                if hasattr(run_model, 'check'):
                    return run_model.check()
                else:
                    print("LM Studio check function is not available in run_model.py.")
                    return False

            except Exception as e:
                print(f"Error checking LM Studio: {e}")
                return False
        else:
            print("LM Studio directory or run_model.py does not exist.")
            return False

    def run_lm_studio(self, user_message):
        """Run the LM Studio AI model."""
        try:
            # Load the run_model.py module dynamically from the lm_studio directory
            spec = importlib.util.spec_from_file_location("run_model", self.lm_studio_path)
            run_model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_model)

            # Ensure the run_model has a process_input function
            if hasattr(run_model, 'process_input'):
                # Call the process_input function with the user_message
                return run_model.process_input(user_message)
            else:
                print(f"LM Studio does not have a process_input function.")
                return "Error: LM Studio is not properly configured."
        except Exception as e:
            print(f"Error running LM Studio: {e}")
            return "Error processing your request with LM Studio."

    ######## END LM STUDIO #######


    ####### LOCAL MODELS #######

    def check_local_model(self):
        """Check if the local model is available and everything is valid."""
        if os.path.exists(self.local_model_path):
            try:
                # Load the run_model.py module dynamically
                spec = importlib.util.spec_from_file_location("run_model", self.local_model_path)
                run_model = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(run_model)

                # Call the 'check' function from run_model
                if hasattr(run_model, 'check'):
                    return run_model.check()
                else:
                    print("Local model check function is not available in run_model.py.")
                    return False

            except Exception as e:
                print(f"Error checking local model: {e}")
                return False
        else:
            print("Local model directory or run_model.py does not exist.")
            return False

    def run_local_model(self, user_message):
        """Run the local AI model."""
        try:
            # Load the run_model.py module dynamically from the ai directory
            spec = importlib.util.spec_from_file_location("run_model", self.local_model_path)
            run_model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(run_model)

            # Ensure the run_model has a process_input function
            if hasattr(run_model, 'process_input'):
                # Call the process_input function with the user_message
                return run_model.process_input(user_message)
            else:
                print(f"Local model does not have a process_input function.")
                return "Error: Local model is not properly configured."
        except Exception as e:
            print(f"Error running Local AI model: {e}")
            return "Error processing your request with the local model."

    ######## END LOCAL MODELS #######


    ####### FALLBACK USER INPUT #######

    def run_user_input(self, user_message):
        """Fallback method: Get bot response from user input (manual input as AI)."""
        print(f"User: {user_message}")
        bot_response = input("Your response as AI: ")
        return bot_response

    ######## END FALLBACK USER INPUT #######
