function getMenuRecommendation() {
    const protein = document.getElementById('protein').value;
    const vegetable = document.getElementById('vegetable').value;
    const taste = document.getElementById('taste_profile').value;

    let recommendedMenu = "ยังคิดไม่ออกเลยค่ะ ลองเลือกวัตถุดิบอื่นนะคะ";
    let reasoning = "AI กำลังเรียนรู้เพิ่มเติมค่ะ";

    // --- นี่คือส่วน "จำลอง" Logic ของ AI แบบง่ายมากๆ ---
    if (protein === 'chicken' && vegetable === 'basil' && (taste === 'spicy' || taste === 'any')) {
        recommendedMenu = "ผัดกะเพราไก่";
        reasoning = "ไก่กับใบกะเพราเป็นส่วนผสมสุดคลาสสิกสำหรับเมนูยอดฮิตรสชาติจัดจ้านค่ะ";
    } else if (protein === 'shrimp' && taste === 'sour' && (vegetable === 'mixed_veg' || vegetable === 'none')) {
        recommendedMenu = "ต้มยำกุ้ง";
        reasoning = "กุ้งสดๆ กับรสต้มยำเปรี้ยวเผ็ดร้อน เป็นอะไรที่ลงตัวสุดๆ สำหรับคนชอบรสจัดค่ะ";
    } else if (protein === 'pork' && vegetable === 'kale' && (taste === 'any')) {
        recommendedMenu = "คะน้าหมูกรอบ";
        reasoning = "หมูกรอบๆ ผัดกับคะน้าสดๆ เป็นเมนูอร่อยทานง่าย ได้ทุกเมื่อค่ะ (AI แนะนำให้เพิ่มหมูกรอบนะคะ!)";
    } else if (protein === 'tofu' && vegetable === 'mixed_veg' && (taste === 'any' || taste === 'spicy')) {
        recommendedMenu = "เต้าหู้ผัดพริกเกลือ (เจ)";
        reasoning = "เต้าหู้ทอดกรอบนอกนุ่มใน คลุกเคล้าเครื่องพริกเกลือรสเด็ด เป็นเมนูมังสวิรัติ/เจ ที่น่าลองค่ะ";
    } else if (protein !== 'none' && vegetable !== 'none') {
        recommendedMenu = `ผัด${vegetable === 'basil' ? 'กะเพรา' : (vegetable === 'morning_glory' ? 'ผักบุ้ง' : 'ผัก')}${protein === 'chicken' ? 'ไก่' : (protein === 'pork' ? 'หมู' : (protein === 'shrimp' ? 'กุ้ง' : 'เต้าหู้'))}`;
        reasoning = "เป็นการผสมผสานวัตถุดิบที่คุณเลือกได้น่าสนใจ AI แนะนำเมนูผัดเบื้องต้นให้ค่ะ";
    }
    // --- สิ้นสุดส่วนจำลอง Logic ---

    document.getElementById('menuName').textContent = recommendedMenu;
    document.getElementById('menuReasoning').textContent = reasoning;
    document.getElementById('recommendationResult').style.display = 'block';
}
