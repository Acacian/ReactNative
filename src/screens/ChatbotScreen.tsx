import React, { useState, useRef } from 'react';
import { View, StyleSheet, FlatList, Dimensions } from 'react-native';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import Header from '../components/Header';
import Footer from '../components/Footer';
import AIEngine from '../models/AIEngine';

const ChatbotScreen = () => {
  const [messages, setMessages] = useState<Array<{ id: string; text: string; isBot: boolean }>>([]);
  const aiEngine = useRef(new AIEngine()).current;

  const handleSendMessage = async (text: string) => {
    // 사용자 메시지 추가
    setMessages(prevMessages => [
      ...prevMessages,
      { id: Date.now().toString(), text, isBot: false }
    ]);

    try {
      const response = await aiEngine.sendMessage(text);

      // AI 응답 추가
      setMessages(prevMessages => [
        ...prevMessages,
        { id: (Date.now() + 1).toString(), text: response, isBot: true }
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
      <FlatList
        style={styles.chatContainer}
        data={messages}
        renderItem={({ item }) => <ChatMessage message={item.text} isBot={item.isBot} />}
        keyExtractor={item => item.id}
      />
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