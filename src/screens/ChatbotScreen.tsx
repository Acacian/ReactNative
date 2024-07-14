import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import AIEngine from '../models/AIEngine';

const ChatbotScreen = () => {
  const [inputText, setInputText] = useState('');
  const [responseText, setResponseText] = useState('');

  const aiEngine = new AIEngine();

  const handleSend = async () => {
    try {
      const response = await aiEngine.predict(inputText);
      setResponseText(response);
    } catch (error) {
      setResponseText('Error occurred');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Chatbot</Text>
      <TextInput
        style={styles.input}
        value={inputText}
        onChangeText={setInputText}
        placeholder="Type your message"
      />
      <Button title="Send" onPress={handleSend} />
      <Text style={styles.response}>{responseText}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  title: {
    fontSize: 24,
    marginBottom: 16,
  },
  input: {
    borderWidth: 1,
    padding: 8,
    marginBottom: 16,
  },
  response: {
    marginTop: 16,
    fontSize: 18,
  },
});

export default ChatbotScreen;
