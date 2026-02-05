import { cn } from "@/lib/utils";

interface ChatMessageProps {
    message: string;
    isUser: boolean;
}

export function ChatMessage({ message, isUser }: ChatMessageProps) {
    return (
        <div
            className={cn(
                "flex w-full mb-4",
                isUser ? "justify-end" : "justify-start"
            )}
        >
            <div
                className={cn(
                    "max-w-[80%] rounded-lg px-4 py-2",
                    isUser
                        ? "bg-primary text-primary-foreground rounded-br-none"
                        : "bg-muted text-foreground rounded-bl-none"
                )}
            >
                <p className="text-sm whitespace-pre-wrap">{message}</p>
            </div>
        </div>
    );
}
