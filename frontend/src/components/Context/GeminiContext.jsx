import { createContext,useState } from "react";
import runChat from "../../config/geminiapi";
import { useMutation } from "react-query";

export const GeminiContext = createContext();

const ContextProvider = (props)=>{
    const [input,setInput]= useState('');
    const [loading, setLoading] = useState(false);
    const [result,setResult]= useState('');
    const [prevPrompt, setPrevPrompt] = useState([]);
    const [recentPrompt, setRecentPrompt] = useState('');
    const [showResult, setshowResult] = useState(false);
    const [messages, setMessages] = useState({
      text: [],
      images: [],
      videos: [],
      memes: [],
    });
    const [extend, setExtend] = useState(null);
    const [summary, setSummary] = useState('')
    const [summaryResult, setSummaryResult] = useState('')
    const [isOpen, setIsOpen] = useState(true);
    const [prompt, setPrompt] = useState("")


    const handleSummarySubmit = async (query) => {
      if (!query.trim()) return;
      setLoading(true)
      
      try {
        const response = await handleOutputSubmit(query,'summary');
        setSummaryResult(response);
        setLoading(false)
      } catch (error) {
        console.error(error);
      }
    };
   

   


    const delayProvider =(index,nextWord)=>{
            setTimeout(function(){
                setResult(prev=>prev+nextWord)
            }, 70*index)
    }
    //for the sidebar button to make new chat and land on the chatbot
    const newChatbtn=()=>{
        setSummaryResult("")
        setIsOpen(true)
        
    }

    const handleRegenerate = async (index) => {
      // Identify the current page's messages
      const pageMessages = messages[currentPage];
      
      // Get the specific message to regenerate
      const messageToRegenerate = pageMessages[index];
    
      if (!messageToRegenerate) return;
    
      // Add a temporary placeholder for the regenerated response
      const tempMessage = { role: "chatbot", text: "", loading: true };
    
      // Update the state to show the loading state
      setMessages((prev) => {
        const updatedMessages = { ...prev };
        updatedMessages[currentPage] = [
          ...pageMessages.slice(0, index),
          tempMessage,
          ...pageMessages.slice(index + 1),
        ];
        return updatedMessages;
      });
    
      try {
        // Fetch the regenerated response
        const regeneratedResponse = await handleOutputSubmit(messageToRegenerate.text);
    
        // Update the state with the regenerated response
        setMessages((prev) => {
          const updatedMessages = { ...prev };
          updatedMessages[currentPage] = [
            ...pageMessages.slice(0, index),
            { role: "chatbot", text: regeneratedResponse, loading: false },
            ...pageMessages.slice(index + 1),
          ];
          return updatedMessages;
        });
      } catch (error) {
        console.error("Error regenerating message:", error);
        setMessages((prev) => {
          const updatedMessages = { ...prev };
          updatedMessages[currentPage] = [
            ...pageMessages.slice(0, index),
            { role: "chatbot", text: "Error: Unable to regenerate message.", loading: false },
            ...pageMessages.slice(index + 1),
          ];
          return updatedMessages;
        });
      }
    };
    
    


    const handleInputSubmit = async (query, page) => {
      if (!query.trim()) return;
      setshowResult(true)
      const userMessage = { role: "user", text: query };
      const tempMessage = { role: "chatbot", text: "", loading: true };
      setMessages((prev) => ({
        ...prev,
        [page]: [...prev[page], userMessage, tempMessage],
      }));
      setPrompt("")
      try {
        const response = await handleOutputSubmit(query,page);
        setMessages((prev) => {
          const updatedPageMessages = [...prev[page]];
          updatedPageMessages[updatedPageMessages.length - 1] = {
            role: "chatbot",
            text: response,
            loading: false,
          };
    
          return { ...prev, [page]: updatedPageMessages };
        });
        console.log(messages)
      } catch (error) {
        console.error(error);
      }
    };
    
      const handleOutputSubmit = async (query,page) => {
        try {
          const response = await runChat(query,page); // Replace with your AI API call
          console.log(response)
          return response;
        } catch (error) {
          console.error("Error fetching AI response:", error);
          return "Something went wrong. Please try again.";
        }
      };
      


    const onSent=async (query)=>{
        setResult('');
        setLoading(true);
        setshowResult(true)
        let response;
        if(prompt===undefined){
            setRecentPrompt(prompt)
            prompt("")
            setPrevPrompt(prev=>[input,...prev])
            response = await runChat(prompt);
        }
        else{
            setRecentPrompt(prompt)
            response = await runChat(prompt);

        }
        
        let responseArray = response.split('**');
        
        for (let i = 0;i<responseArray.length;i++){
            const nextWord = responseArray[i];
            delayProvider(i,nextWord+" ");
        }
        setLoading(false);
        

    }
    // onSent('What is react?');

    // const onSent = async (prompt) => {
    //     setLoading(true);
    //     setshowResult(true);
    
    //     if (prompt === undefined) {
    //         // Handling user input
    //         setRecentPrompt(input);
    //         setInput("");
    //         setMessages((prevMessages) => [
    //             ...prevMessages,
    //             { type: "user", text: input }, // Add user message
    //         ]);
    //         prompt = input; // Use the user input as the prompt
    //     } else {
    //         // Handling a specific prompt (e.g., predefined or history-based)
    //         setRecentPrompt(prompt);
    //     }
    
    //     // Run chat and get the AI response
    //     let response = await runChat(prompt);
    
    //     // Process response into chunks (if applicable)
    //     let responseArray = response.split("**");
    
    //     // Add each response chunk as a separate AI message with delay
    //     responseArray.forEach((chunk, index) => {
    //         delayProvider(index, () => {
    //             setMessages((prevMessages) => [
    //                 ...prevMessages,
    //                 { type: "ai", text: chunk.trim() }, // Add AI response
    //             ]);
    //         });
    //     });
    
    //     setLoading(false);
    // };
    

    const contextValue = {
      extend, setExtend,
      isOpen, setIsOpen,
      summaryResult, setSummaryResult,
      handleSummarySubmit,
      handleRegenerate,
        handleInputSubmit,
        messages, setMessages,
        prompt, setPrompt,
        setInput,
        loading,
        setLoading,
        result,
        setResult,
        prevPrompt,
        setPrevPrompt,
        recentPrompt,
        setRecentPrompt,
        showResult,
        setshowResult,
        onSent,
        newChatbtn,
    }
    return(

        <GeminiContext.Provider value={contextValue}>
            {props.children}
        </GeminiContext.Provider>
    )
}

export default ContextProvider;