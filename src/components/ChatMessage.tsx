import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

type ChatMessageProps = {
  message: string;
  isBot: boolean;
};

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isBot }) => {
  return (
    <View style={[styles.container, isBot ? styles.bot : styles.user]}>
      <Text style={isBot ? styles.botText : styles.userText}>{message}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 10,
    marginVertical: 5,
    borderRadius: 10,
    maxWidth: '80%',
  },
  bot: {
    backgroundColor: '#e0e0e0',
    alignSelf: 'flex-start',
  },
  user: {
    backgroundColor: '#0084ff',
    alignSelf: 'flex-end',
  },
  botText: {
    color: '#000',
  },
  userText: {
    color: '#fff',
  },
});

export default ChatMessage;
