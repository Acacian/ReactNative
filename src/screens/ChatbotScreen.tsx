import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Dimensions } from 'react-native';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import Header from '../components/Header';
import Footer from '../components/Footer';

const API_URL = 'http://localhost:5000/predict';  // Docker 환경에 맞게 URL을 수정하세요

const ChatbotScreen = () => {
  const [messages, setMessages] = useState<Array<{ id: string; text: string; isBot: boolean }>>([]);

  const handleSendMessage = async (text: string) => {
    // 사용자 메시지 추가
    setMessages(prevMessages => [
      ...prevMessages,
      { id: Date.now().toString(), text, isBot: false }
    ]);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();

      // AI 응답 추가
      setMessages(prevMessages => [
        ...prevMessages,
        { id: (Date.now() + 1).toString(), text: data.response, isBot: true }
      ]);
    } catch (error) {
      console.error('Error calling API:', error);
      // 오류 메시지 표시
      setMessages(prevMessages => [
        ...prevMessages,
        { id: (Date.now() + 1).toString(), text: "죄송합니다. 오류가 발생했습니다.", isBot: true }
      ]);
    }
  };

  return (
    <View style={styles.container}>
      <Header />
      <ScrollView style={styles.chatContainer}>
        {messages.map(message => (
          <ChatMessage key={message.id} message={message.text} isBot={message.isBot} />
        ))}
      </ScrollView>
      <ChatInput onSendMessage={handleSendMessage} />
      <Footer />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    height: Dimensions.get('window').height,
  },
  chatContainer: {
    flex: 1,
    padding: 10,
  },
});

export default ChatbotScreen;