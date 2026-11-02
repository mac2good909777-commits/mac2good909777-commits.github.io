export const SITE = {
  title: '張現傑 × 睦聚地產｜工業不動產',
  description: '工業不動產市場觀察・產業資訊分析・前期判讀整理。張現傑 × 睦聚地產長期內容累積平台。',
  author: '張現傑',
  tagline: '工業不動產・市場觀察・產業資訊分析',
  licenseNo: '不動產經紀人｜登錄字號：（請填入）',
  contact: {
    line: 'https://line.me/ti/p/~0953909777',
    phone: '0953-909-777',
    email: 'a.ruei.he@gmail.com',
    fbPage: 'https://www.facebook.com/industrial.realestate.notes',
  },
  workHours: '平日 09:00–21:00 優先回覆，假日視情況',
};

export type CategoryKey = 'industry-data' | 'market-view' | 'insights';

export const CATEGORIES: Record<CategoryKey, {
  name: string;
  subtitle: string;
  description: string;
  color: string;
  colorSoft: string;
  ariaLabel: string;
}> = {
  'industry-data': {
    name: '產業資訊',
    subtitle: '工業地段與廠房的實價登錄彙整與資料判讀',
    description: '以資料與數據為主的分類 — 實價登錄彙整、特定工業區交易資料、價格區間整理。這裡不做花俏的預測，讓數字自己說話。',
    color: '#1E3A5F',
    colorSoft: '#EBF2FA',
    ariaLabel: '產業資訊分類',
  },
  'market-view': {
    name: '市場觀察',
    subtitle: '工業不動產市場趨勢與佈局觀察',
    description: '第一人稱的深度觀點 — 趨勢判讀、產業佈局、買方結構變化。寫我觀察到的事，而不是我聽到的事。',
    color: '#2B5A8C',
    colorSoft: '#EBF2FA',
    ariaLabel: '市場觀察分類',
  },
  insights: {
    name: '其他資訊',
    subtitle: '不動產相關的實用工具、法規與風險提醒',
    description: '實用型內容 — 法規指南、工具攻略、風險防範、操作步驟。適合有具體問題要解決的讀者。',
    color: '#D97706',
    colorSoft: '#FEF3E6',
    ariaLabel: '其他資訊分類',
  },
};

export const NAV_ITEMS = [
  { href: '/about/', label: '關於我' },
  { href: '/industry-data/', label: '產業資訊' },
  { href: '/market-view/', label: '市場觀察' },
  { href: '/insights/', label: '其他資訊' },
  { href: '/contact/', label: '聯繫' },
];
