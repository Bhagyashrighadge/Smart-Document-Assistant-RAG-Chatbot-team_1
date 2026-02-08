"""
Mock Response Generator for Testing Language Control
Provides language-appropriate responses for testing without API calls
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Test responses in different languages
MOCK_RESPONSES: Dict[str, Dict[str, str]] = {
    "en": {
        "default": "Based on the document content, artificial intelligence (AI) is the simulation of human intelligence in machines. It enables computers to think, learn, and make decisions like humans. AI systems can analyze large amounts of data quickly and provide insights. AI is used in healthcare for disease detection, in education for personalized learning, and in business for customer service automation.",
        "what is ai": "Artificial Intelligence is the simulation of human intelligence in machines that enables computers to perform tasks that typically require human intelligence. This includes learning from experience, recognizing patterns, understanding language, and making decisions.",
        "what is machine learning": "Machine Learning is a subset of AI where systems learn from data without being explicitly programmed. It uses algorithms to analyze patterns in data and make predictions or decisions based on those patterns.",
        "what is cloud computing": "Cloud computing is the delivery of computing services over the internet, including servers, storage, databases, and software. It allows organizations to access these resources on-demand without owning physical infrastructure.",
    },
    "hi": {
        "default": "दस्तावेज़ की सामग्री के अनुसार, कृत्रिम बुद्धिमत्ता (AI) मशीनों में मानव बुद्धिमत्ता का अनुकरण है। यह कंप्यूटर को मनुष्यों की तरह सोचने, सीखने और निर्णय लेने में सक्षम बनाता है। AI सिस्टम तेजी से बड़ी मात्रा में डेटा का विश्लेषण कर सकते हैं। AI का उपयोग स्वास्थ्यसेवा में बीमारी की पहचान के लिए, शिक्षा में व्यक्तिगत सीखने के लिए, और व्यापार में ग्राहक सेवा स्वचालन के लिए किया जाता है।",
        "what is ai": "कृत्रिम बुद्धिमत्ता मशीनों में मानव बुद्धिमत्ता का अनुकरण है जो कंप्यूटर को उन कार्यों को करने में सक्षम बनाता है जिनमें आम तौर पर मानव बुद्धिमत्ता की आवश्यकता होती है। इसमें अनुभव से सीखना, पैटर्न पहचानना, भाषा समझना और निर्णय लेना शामिल है।",
        "what is machine learning": "मशीन लर्निंग AI का एक उपसमूह है जहां सिस्टम बिना स्पष्ट रूप से प्रोग्राम किए डेटा से सीखते हैं। यह डेटा में पैटर्न का विश्लेषण करने और उन पैटर्न के आधार पर भविष्यवाणी या निर्णय लेने के लिए एल्गोरिदम का उपयोग करता है।",
        "what is cloud computing": "क्लाउड कंप्यूटिंग इंटरनेट पर कंप्यूटिंग सेवाओं की डिलीवरी है, जिसमें सर्वर, स्टोरेज, डेटाबेस और सॉफ्टवेयर शामिल हैं। यह संगठनों को इन संसाधनों को भौतिक बुनियादी ढांचे के मालिक हुए बिना मांग पर एक्सेस करने की अनुमति देता है।",
    },
    "mr": {
        "default": "दस्तऐवजाच्या मजकूराप्रमाणे, कृत्रिम बुद्धिमत्ता (AI) हे मशीनमधील मानवी बुद्धिमत्तेचे अनुकरण आहे. हे संगणकांना मानवांसारखे विचार करण्यास, शिकण्यास आणि निर्णय घेण्यास सक्षम बनवते. AI प्रणाली द्रुतगतीने मोठ्या प्रमाणात डेटाचे विश्लेषण करू शकतात. AI चा वापर आरोग्यसेवेत रोगाचे निदान करण्यासाठी, शिक्षणात वैयक्तिक शिक्षणासाठी आणि व्यावसायिकतेत ग्राहक सेवा स्वयंचलितासाठी केला जातो.",
        "what is ai": "कृत्रिम बुद्धिमत्ता मशीनमधील मानवी बुद्धिमत्तेचे अनुकरण आहे जे संगणकांना अशा कार्यांचे निर्वहन करण्यास सक्षम बनवते ज्यांसाठी सामान्यतः मानवी बुद्धिमत्तेची आवश्यकता असते. यामध्ये अनुभवातून शिकणे, नमुने ओळखणे, भाषा समजणे आणि निर्णय घेणे समाविष्ट आहे.",
        "what is machine learning": "मशीन लर्निंग हे AI चा एक उपसंच आहे जेथे प्रणाली स्पष्टपणे प्रोग्राम केल्याशिवाय डेटामधून शिकतात. हे डेटामधील नमुने विश्लेषण करण्यास आणि त्या नमुन्यांवर आधारित भविष्यवाणी किंवा निर्णय घेण्यास अल्गोरिदम वापरते.",
        "what is cloud computing": "क्लाउड संगणन हे इंटरनेटवर संगणन सेवांची वितरण आहे, ज्यामध्ये सर्व्हर, स्टोरेज, डेटाबेस आणि सॉफ्टवेअर समाविष्ट आहेत. हे संस्थांना भौतिक अवसंरचना मालकीचे न होता मागणीवर या संसाधनांचा वापर करण्याची अनुमती देते.",
    }
}


def get_mock_response(language: str, question: str = "", context: str = "") -> str:
    """
    Get a mock response in the specified language
    
    Args:
        language: Language code ('en', 'hi', 'mr')
        question: User question (used to match specific responses)
        context: Document context (not used in mock, but kept for interface compatibility)
        
    Returns:
        Mock response in the requested language
    """
    if language not in MOCK_RESPONSES:
        language = "en"
    
    responses = MOCK_RESPONSES[language]
    
    # Try to match question to specific response
    question_lower = question.lower()
    for key in responses.keys():
        if key != "default" and key in question_lower:
            logger.info(f"[MOCK] Returning matched response for: {key}")
            return responses[key]
    
    # Default response
    logger.info(f"[MOCK] Returning default response for language: {language}")
    return responses["default"]


def enable_mock_mode(service):
    """
    Monkeypatch a DeepSeekService instance to use mock responses
    
    Args:
        service: DeepSeekService instance to patch
    """
    logger.warning("[MOCK_MODE] Enabling mock response generation - NO API CALLS WILL BE MADE")
    
    def mocked_generate(prompt, context="", language="en", **kwargs):
        """Mock implementation of generate_response"""
        logger.info(f"[MOCK] Generating response in {language}")
        logger.info(f"[MOCK] Question: {prompt[:100]}...")
        
        response = get_mock_response(language, prompt, context)
        logger.info(f"[MOCK] Response length: {len(response)} characters")
        return response
    
    service.generate_response = mocked_generate
    logger.info("[MOCK_MODE] Service ready - using mock responses for all API calls")
