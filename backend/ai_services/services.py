import openai
import base64
import json
import time
from typing import Dict, List, Tuple, Optional
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
import io
import requests
from .models import AIWasteClassification, AIChatConversation, AIChatMessage, AIModelPerformance
from items.models import Item, Category

class WasteClassificationService:
    """خدمة تصنيف المخلفات بالذكاء الاصطناعي"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4-vision-preview"
        
        # قاموس الفئات بالعربية والإنجليزية
        self.categories_map = {
            'furniture': 'أثاث',
            'electronics': 'إلكترونيات', 
            'metals': 'معادن',
            'plastic': 'بلاستيك',
            'paper': 'ورق وكرتون',
            'glass': 'زجاج',
            'textiles': 'منسوجات',
            'construction': 'مواد بناء',
            'organic': 'مخلفات عضوية',
            'hazardous': 'مواد خطرة'
        }
        
        # نصائح إعادة التدوير
        self.recycling_tips = {
            'plastic': 'تأكد من تنظيف البلاستيك قبل إعادة التدوير. فصل الأنواع المختلفة حسب الرمز.',
            'paper': 'أزل أي مواد لاصقة أو معدنية. تجنب الورق المبلل أو الملوث.',
            'metals': 'فصل المعادن المختلفة. الألومنيوم والنحاس لهما قيمة عالية.',
            'electronics': 'احذف البيانات الشخصية. فصل البطاريات. ابحث عن مراكز متخصصة.',
            'glass': 'فصل الألوان المختلفة. أزل الأغطية المعدنية أو البلاستيكية.',
            'furniture': 'فكك القطع الكبيرة. فصل المواد المختلفة (خشب، معدن، قماش).',
            'textiles': 'تبرع بالملابس الصالحة. استخدم الباقي كخرق أو لإعادة التدوير.',
            'construction': 'فصل المواد المختلفة. بعض المواد قابلة لإعادة الاستخدام مباشرة.'
        }
    
    def encode_image(self, image_path: str) -> str:
        """تحويل الصورة إلى base64"""
        try:
            if image_path.startswith('http'):
                response = requests.get(image_path)
                image_data = response.content
            else:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
            
            return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            raise Exception(f"خطأ في تحويل الصورة: {str(e)}")
    
    def classify_waste_image(self, image_path: str, item_description: str = "") -> Dict:
        """تصنيف صورة المخلفات"""
        start_time = time.time()
        
        try:
            # تحويل الصورة
            base64_image = self.encode_image(image_path)
            
            # إعداد الرسالة للـ AI
            messages = [
                {
                    "role": "system",
                    "content": """أنت خبير في تصنيف المخلفات وإعادة التدوير. مهمتك تحليل الصور وتصنيف المخلفات بدقة عالية.

يجب أن تقوم بما يلي:
1. تحديد نوع المخلف الرئيسي
2. تقدير نسبة الثقة في التصنيف (0-1)
3. تحليل تركيب المواد
4. تقييم قابلية إعادة التدوير (0-1)
5. تقدير التأثير البيئي (low/medium/high)
6. اقتراح نطاق سعري مناسب
7. تقديم نصائح لإعادة التدوير
8. تحذيرات السلامة إن وجدت

الفئات المتاحة: furniture, electronics, metals, plastic, paper, glass, textiles, construction, organic, hazardous

أجب بصيغة JSON فقط."""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"صنف هذه الصورة للمخلفات. الوصف المرفق: {item_description}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ]
            
            # استدعاء OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.1
            )
            
            # استخراج النتيجة
            result_text = response.choices[0].message.content
            
            # تحويل النتيجة إلى JSON
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # إذا لم يكن JSON صحيح، نحاول استخراج المعلومات
                result = self._parse_ai_response(result_text)
            
            # حساب وقت المعالجة
            processing_time = time.time() - start_time
            
            # تنسيق النتيجة
            formatted_result = self._format_classification_result(result, processing_time)
            
            return formatted_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """تحليل رد AI إذا لم يكن JSON صحيح"""
        # تحليل بسيط للنص واستخراج المعلومات
        result = {
            'category': 'other',
            'confidence': 0.5,
            'material_composition': {},
            'recyclability_score': 0.5,
            'environmental_impact': 'medium',
            'price_range': {'min': 0, 'max': 100},
            'recycling_tips': 'يرجى مراجعة خبير إعادة التدوير',
            'safety_warnings': ''
        }
        
        # محاولة استخراج الفئة من النص
        for category in self.categories_map.keys():
            if category in response_text.lower() or self.categories_map[category] in response_text:
                result['category'] = category
                break
        
        return result
    
    def _format_classification_result(self, result: Dict, processing_time: float) -> Dict:
        """تنسيق نتيجة التصنيف"""
        category = result.get('category', 'other')
        confidence = float(result.get('confidence', 0.5))
        
        # تحديد مستوى الثقة
        if confidence >= 0.95:
            confidence_level = 'very_high'
        elif confidence >= 0.85:
            confidence_level = 'high'
        elif confidence >= 0.70:
            confidence_level = 'medium'
        elif confidence >= 0.50:
            confidence_level = 'low'
        else:
            confidence_level = 'very_low'
        
        return {
            'success': True,
            'predicted_category': category,
            'predicted_category_ar': self.categories_map.get(category, 'غير محدد'),
            'confidence_score': confidence,
            'confidence_level': confidence_level,
            'material_composition': result.get('material_composition', {}),
            'recyclability_score': float(result.get('recyclability_score', 0.5)),
            'environmental_impact': result.get('environmental_impact', 'medium'),
            'suggested_price_range': result.get('price_range', {'min': 0, 'max': 100}),
            'recycling_tips': result.get('recycling_tips', self.recycling_tips.get(category, '')),
            'safety_warnings': result.get('safety_warnings', ''),
            'processing_time': processing_time
        }
    
    def save_classification_result(self, item: Item, image_url: str, result: Dict) -> AIWasteClassification:
        """حفظ نتيجة التصنيف في قاعدة البيانات"""
        if not result.get('success'):
            classification = AIWasteClassification.objects.create(
                item=item,
                image_url=image_url,
                status='failed',
                error_message=result.get('error', 'خطأ غير معروف'),
                processing_time=result.get('processing_time', 0)
            )
            return classification
        
        classification = AIWasteClassification.objects.create(
            item=item,
            image_url=image_url,
            predicted_category=result['predicted_category'],
            predicted_category_ar=result['predicted_category_ar'],
            confidence_score=result['confidence_score'],
            confidence_level=result['confidence_level'],
            material_composition=result['material_composition'],
            recyclability_score=result['recyclability_score'],
            environmental_impact=result['environmental_impact'],
            suggested_price_range=result['suggested_price_range'],
            recycling_tips=result['recycling_tips'],
            safety_warnings=result['safety_warnings'],
            status='completed',
            processing_time=result['processing_time']
        )
        
        # تحديث فئة المنتج إذا كانت الثقة عالية
        if result['confidence_score'] >= 0.85:
            try:
                category = Category.objects.get(name=result['predicted_category'])
                item.category = category
                item.save()
            except Category.DoesNotExist:
                pass
        
        return classification

class AIChatService:
    """خدمة المحادثة الذكية"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4-turbo-preview"
        
        # شخصية المساعد الذكي
        self.system_prompt = """أنت مساعد ذكي متخصص في إعادة التدوير والبيئة في مصر. اسمك "جرين بوت".

خبراتك تشمل:
- تصنيف وتقييم المخلفات
- نصائح إعادة التدوير
- تقدير أسعار المواد المعاد تدويرها
- القوانين البيئية المصرية
- أفضل الممارسات البيئية
- ربط المستخدمين بالورش والمصانع المناسبة

أسلوبك:
- ودود ومفيد
- استخدم اللغة العربية بشكل أساسي
- قدم معلومات دقيقة وعملية
- اسأل أسئلة توضيحية عند الحاجة
- قدم حلول عملية ومحلية

تذكر أنك تعمل في منصة GreenSwap Egypt لربط أصحاب المخلفات بورش إعادة التدوير."""
    
    def create_conversation(self, user, conversation_type: str, title: str, context_data: Dict = None) -> AIChatConversation:
        """إنشاء محادثة جديدة"""
        conversation = AIChatConversation.objects.create(
            user=user,
            conversation_type=conversation_type,
            title=title,
            context_data=context_data or {}
        )
        
        # رسالة ترحيب
        welcome_message = self._get_welcome_message(conversation_type)
        AIChatMessage.objects.create(
            conversation=conversation,
            message_type='ai',
            content=welcome_message
        )
        
        return conversation
    
    def _get_welcome_message(self, conversation_type: str) -> str:
        """رسائل الترحيب حسب نوع المحادثة"""
        messages = {
            'waste_inquiry': 'مرحباً! أنا جرين بوت 🌱 مساعدك في تصنيف وتقييم المخلفات. كيف يمكنني مساعدتك اليوم؟',
            'recycling_advice': 'أهلاً بك! 🔄 أنا هنا لأقدم لك أفضل النصائح لإعادة التدوير. ما نوع المخلفات التي تريد معرفة المزيد عنها؟',
            'price_estimation': 'مرحباً! 💰 سأساعدك في تقدير أسعار المواد المعاد تدويرها. أخبرني عن المواد التي لديك.',
            'general_support': 'أهلاً وسهلاً! 🤝 أنا جرين بوت، مساعدك في كل ما يتعلق بإعادة التدوير والبيئة. كيف يمكنني مساعدتك؟',
            'item_recommendation': 'مرحباً! 🎯 سأساعدك في العثور على أفضل المنتجات والعروض المناسبة لاحتياجاتك. ماذا تبحث عنه؟'
        }
        return messages.get(conversation_type, messages['general_support'])
    
    def send_message(self, conversation: AIChatConversation, user_message: str, attachments: List = None) -> AIChatMessage:
        """إرسال رسالة والحصول على رد AI"""
        start_time = time.time()
        
        # حفظ رسالة المستخدم
        user_msg = AIChatMessage.objects.create(
            conversation=conversation,
            message_type='user',
            content=user_message,
            attachments=attachments or []
        )
        
        try:
            # إعداد سياق المحادثة
            messages = self._build_conversation_context(conversation, user_message)
            
            # استدعاء OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            processing_time = time.time() - start_time
            tokens_used = response.usage.total_tokens
            
            # حفظ رد AI
            ai_msg = AIChatMessage.objects.create(
                conversation=conversation,
                message_type='ai',
                content=ai_response,
                ai_confidence=0.9,  # يمكن حسابها بناءً على نوع الرد
                processing_time=processing_time,
                tokens_used=tokens_used
            )
            
            # تحديث المحادثة
            conversation.updated_at = ai_msg.created_at
            conversation.save()
            
            return ai_msg
            
        except Exception as e:
            # حفظ رسالة خطأ
            error_msg = AIChatMessage.objects.create(
                conversation=conversation,
                message_type='ai',
                content=f"عذراً، حدث خطأ في معالجة رسالتك: {str(e)}",
                ai_confidence=0.0,
                processing_time=time.time() - start_time
            )
            return error_msg
    
    def _build_conversation_context(self, conversation: AIChatConversation, current_message: str) -> List[Dict]:
        """بناء سياق المحادثة للـ AI"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # إضافة سياق خاص بنوع المحادثة
        context_prompt = self._get_context_prompt(conversation.conversation_type, conversation.context_data)
        if context_prompt:
            messages.append({"role": "system", "content": context_prompt})
        
        # إضافة آخر 10 رسائل من المحادثة
        recent_messages = conversation.messages.order_by('-created_at')[:10]
        for msg in reversed(recent_messages):
            role = "user" if msg.message_type == "user" else "assistant"
            messages.append({"role": role, "content": msg.content})
        
        # إضافة الرسالة الحالية
        messages.append({"role": "user", "content": current_message})
        
        return messages
    
    def _get_context_prompt(self, conversation_type: str, context_data: Dict) -> str:
        """سياق إضافي حسب نوع المحادثة"""
        if conversation_type == 'waste_inquiry' and context_data.get('item_id'):
            return f"المستخدم يسأل عن منتج معين (ID: {context_data['item_id']}). قدم معلومات مفصلة ونصائح عملية."
        
        elif conversation_type == 'price_estimation':
            return "ركز على تقدير الأسعار بناءً على السوق المصري الحالي. اعتبر العوامل المحلية مثل الطلب والعرض."
        
        elif conversation_type == 'recycling_advice':
            return "قدم نصائح عملية وقابلة للتطبيق في البيئة المصرية. اذكر أماكن ومراكز إعادة التدوير المحلية إن أمكن."
        
        return ""
    
    def get_conversation_summary(self, conversation: AIChatConversation) -> str:
        """ملخص المحادثة"""
        messages = conversation.messages.all()[:20]  # آخر 20 رسالة
        
        conversation_text = "\n".join([
            f"{'المستخدم' if msg.message_type == 'user' else 'المساعد'}: {msg.content}"
            for msg in messages
        ])
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "لخص هذه المحادثة في 2-3 جمل باللغة العربية."},
                    {"role": "user", "content": conversation_text}
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except:
            return "محادثة حول إعادة التدوير والمخلفات"

class AIRecommendationService:
    """خدمة التوصيات الذكية"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"
    
    def get_item_recommendations(self, user, limit: int = 5) -> List[Dict]:
        """توصيات المنتجات للمستخدم"""
        # جمع بيانات المستخدم
        user_data = self._collect_user_data(user)
        
        # استخدام AI لتحليل التفضيلات
        preferences = self._analyze_user_preferences(user_data)
        
        # البحث عن منتجات مناسبة
        recommended_items = self._find_matching_items(preferences, limit)
        
        return recommended_items
    
    def _collect_user_data(self, user) -> Dict:
        """جمع بيانات المستخدم للتحليل"""
        from items.models import Item
        
        # المنتجات التي أضافها المستخدم
        user_items = Item.objects.filter(user=user).values('category__name', 'condition', 'price_type')
        
        # المنتجات التي أبدى اهتماماً بها
        # interested_items = ... (يحتاج تطبيق نظام الاهتمام)
        
        return {
            'user_type': user.user_type,
            'location': user.location,
            'user_items': list(user_items),
            'preferences': {}  # يمكن إضافة المزيد من البيانات
        }
    
    def _analyze_user_preferences(self, user_data: Dict) -> Dict:
        """تحليل تفضيلات المستخدم باستخدام AI"""
        try:
            prompt = f"""
            حلل بيانات هذا المستخدم واستنتج تفضيلاته:
            
            نوع المستخدم: {user_data['user_type']}
            الموقع: {user_data['location']}
            المنتجات المضافة: {user_data['user_items']}
            
            أجب بصيغة JSON تحتوي على:
            - preferred_categories: قائمة الفئات المفضلة
            - price_range: النطاق السعري المفضل
            - condition_preference: الحالة المفضلة للمنتجات
            - location_preference: تفضيل المواقع
            """
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except:
            # تفضيلات افتراضية
            return {
                'preferred_categories': ['plastic', 'metals', 'electronics'],
                'price_range': {'min': 0, 'max': 1000},
                'condition_preference': ['good', 'excellent'],
                'location_preference': user_data['location']
            }
    
    def _find_matching_items(self, preferences: Dict, limit: int) -> List[Dict]:
        """البحث عن منتجات مناسبة"""
        from items.models import Item
        
        # بناء استعلام قاعدة البيانات بناءً على التفضيلات
        queryset = Item.objects.filter(status='active')
        
        # تصفية حسب الفئات المفضلة
        if preferences.get('preferred_categories'):
            queryset = queryset.filter(category__name__in=preferences['preferred_categories'])
        
        # تصفية حسب الحالة
        if preferences.get('condition_preference'):
            queryset = queryset.filter(condition__in=preferences['condition_preference'])
        
        # تصفية حسب الموقع
        if preferences.get('location_preference'):
            queryset = queryset.filter(location__icontains=preferences['location_preference'])
        
        # ترتيب وتحديد العدد
        items = queryset.order_by('-created_at')[:limit]
        
        return [
            {
                'id': item.id,
                'title': item.title,
                'category': item.category.name_ar,
                'price': str(item.price) if item.price else 'مجاني',
                'location': item.location,
                'confidence': 0.8  # يمكن حسابها بطريقة أكثر تعقيداً
            }
            for item in items
        ]
