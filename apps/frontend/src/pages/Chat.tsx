import { useState, useRef, useEffect } from 'react';
import api from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ChatMessage } from '@/components/ChatMessage';
import { Send, Loader2 } from 'lucide-react';

interface Message {
    text: string;
    isUser: boolean;
    timestamp: number;
}

export default function Chat() {
    const [messages, setMessages] = useState<Message[]>([
        { text: "Hello! I'm your AI Stylist. How can I help you regarding fashion today?", isUser: false, timestamp: Date.now() }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!inputValue.trim() || loading) return;

        const userMessage = inputValue.trim();
        setInputValue('');
        setLoading(true);

        // Add user message
        setMessages(prev => [...prev, { text: userMessage, isUser: true, timestamp: Date.now() }]);

        try {
            const response = await api.post('/chat', { message: userMessage });

            // Add AI response
            setMessages(prev => [...prev, {
                text: response.data.response,
                isUser: false,
                timestamp: Date.now()
            }]);
        } catch (error) {
            console.error('Failed to send message:', error);
            setMessages(prev => [...prev, {
                text: "I'm sorry, I'm having trouble connecting to the server. Please try again later.",
                isUser: false,
                timestamp: Date.now()
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container max-w-2xl mx-auto p-4 h-[calc(100vh-2rem)] flex flex-col">
            <Card className="flex-1 flex flex-col overflow-hidden">
                <CardHeader className="border-b">
                    <CardTitle className="flex items-center gap-2">
                        <span className="text-xl">✨</span> AI Stylist
                    </CardTitle>
                </CardHeader>

                <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
                    {messages.map((msg, idx) => (
                        <ChatMessage
                            key={`${msg.timestamp}-${idx}`}
                            message={msg.text}
                            isUser={msg.isUser}
                        />
                    ))}
                    {loading && (
                        <div className="flex justify-start mb-4">
                            <div className="bg-muted text-foreground rounded-lg rounded-bl-none px-4 py-2 flex items-center gap-2">
                                <Loader2 className="h-4 w-4 animate-spin" />
                                <span className="text-xs text-muted-foreground">Thinking...</span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </CardContent>

                <div className="p-4 border-t bg-background">
                    <form onSubmit={handleSendMessage} className="flex gap-2">
                        <Input
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Ask for outfit advice..."
                            disabled={loading}
                            className="flex-1"
                        />
                        <Button type="submit" size="icon" disabled={loading || !inputValue.trim()}>
                            <Send className="h-4 w-4" />
                        </Button>
                    </form>
                </div>
            </Card>
        </div>
    );
}
