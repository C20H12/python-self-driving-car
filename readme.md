# Neural Network Controlled Car in Pygame
___

### Setup
1. Run `main.py`
2. Choose a controlling option
3. If AI controlled, choose a model
4. Confirm to begin session

### In session
- If manual, use WASD or Arrow Keys to move
- Use R to reload session
- Use Q to quit session, the session will be deleted
- Use Z to save a model, this will overwrite a model saved in this session
- Use X to delete a model saved in this session

### Features
- Modualar: The Car, Road, and the Network can be tweeked to a custom setup
- Good visualizations: Allows the user to see exactly how the network is functioning and iterating
- Maintainable: Sections of code are isolated

### Improvements
- Self training: The script will be able to auto reload after a certain threashold save the most optimal model after serveral iterations
- Variable road: Allow more factors of the road to be controlled and altered, ie. adding lanes or curves
- Intelligent traffic: Instead of dummy cars that only goes forward, give the traffic AI brains as well