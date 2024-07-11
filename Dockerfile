# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in package.json
RUN npm install

# Install react-native CLI globally
RUN npm install -g react-native-cli

# Expose port 8081 for React Native Packager
EXPOSE 8081

# Command to run when the container starts
CMD ["npm", "start"]
