import os
import torch
import soundfile as sf
from transformers import AutoTokenizer, AutoModelForCausalLM

# ================= 1. 路径配置 =================
# 基础模型路径（Step 11000，包含分词器配置文件）
BASE_PATH = r"pretrained_models/Spark-TTS-0.5B/LLM" 
# 微调后的最佳检查点（Step 15000）
CHECKPOINT_PATH = "./outputs/out/checkpoint-15000"
# 输出目录
OUTPUT_DIR = "./results_kk"
device = "cuda" if torch.cuda.is_available() else "cpu"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ================= 2. 测试用例（短句 vs 长句） =================
test_cases = {
    "short": [
        "Сәлеметсіз бе! Қалыңыз қалай?",  # 你好！你好吗？
        "Бүгін Астанада ауа райы өте жақсы.", # 今天阿斯塔纳天气很好
        "Кеш жарық, достар!" # 晚上好，朋友们
    ],
    "long": [
        "Қазақстанның елордасы — Астана қаласы, ол еліміздің орталық бөлігінде орналасқан және қарқынды дамып келе жатқан заманауи мегаполис.",
        "Біздің басты мақсатымыз — сапалы білім алу және жаңа технологияларды меңгеру арқылы еліміздің болашағын жарқын ету.",
        "Тәуелсіздік — біздің ең басты құндылығымыз, оны сақтау және нығайту әрбір азаматтың қасиетті борышы болып саналады."
    ]
}

# ================= 3. 加载模型 =================
print(f"Loading tokenizer from base: {BASE_PATH}")
# 核心修正：使用基础模型的路径加载分词器
tokenizer = AutoTokenizer.from_pretrained(BASE_PATH)

print(f"Loading finetuned model from: {CHECKPOINT_PATH}")
# 使用 AutoModelForCausalLM 加载（因为 Qwen2 是因果语言模型架构）
model = AutoModelForCausalLM.from_pretrained(CHECKPOINT_PATH, device_map="auto").to(device)
model.eval()

# ================= 4. 执行生成 =================


@torch.no_grad()
def tts_inference(text, filename):
    print(f"Generating: {text[:20]}...")
    
    # 编码文本
    inputs = tokenizer(text, return_tensors="pt").to(device)
    
    # 调用生成接口
    # 注意：Spark-TTS 的生成方法可能包含特定的参数（如 prompt_speech）
    # 这里使用通用的 generate，如果模型有专门的推理函数请替换
    outputs = model.generate(**inputs, max_new_tokens=512) 
    
    # 假设模型输出直接包含音频波形（或需经过 VAE 解码）
    # 此处逻辑需根据 Spark-TTS 官方推理示例的后处理步骤调整
    audio_data = outputs.cpu().numpy().squeeze()
    
    save_path = os.path.join(OUTPUT_DIR, filename)
    sf.write(save_path, audio_data, 16000) # 采样率通常为 16k 或 24k
    print(f"Successfully saved to {save_path}")

# 循环测试
for category, sentences in test_cases.items():
    print(f"\n--- Testing {category} sentences ---")
    for i, txt in enumerate(sentences):
        file_name = f"kazakh_{category}_{i+1}.wav"
        tts_inference(txt, file_name)

print("\nAll inference tasks completed!")