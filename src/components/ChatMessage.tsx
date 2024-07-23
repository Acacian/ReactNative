import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

type ChatMessageProps = {
  message: string;
  isBot: boolean;
};

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isBot }) => {
  return (
    <View style={[styles.container, isBot ? styles.botContainer : styles.userContainer]}>
      <Text style={[styles.text, isBot ? styles.botText : styles.userText]}>{message}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    maxWidth: '80%',
    padding: 10,
    borderRadius: 10,
    marginBottom: 10,
  },
  botContainer: {
    alignSelf: 'flex-start',
    backgroundColor: '#E5E5EA',
  },
  userContainer: {
    alignSelf: 'flex-end',
    backgroundColor: '#007AFF',
  },
  text: {
    fontSize: 16,
  },
  botText: {
    color: '#000',
  },
  userText: {
    color: '#FFF',
  },
});

export default ChatMessage;