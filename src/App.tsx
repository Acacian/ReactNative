import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './screens/HomeScreen';
import ChatbotScreen from './screens/ChatbotScreen';

export type RootStackParamList = {
  Home: undefined;
  Chatbot: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Home' }} />
        <Stack.Screen name="Chatbot" component={ChatbotScreen} options={{ title: 'AI Chatbot' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;