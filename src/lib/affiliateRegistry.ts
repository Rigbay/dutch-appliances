import { readFileSync } from 'fs';

// Use committed registry copy (sync from ~/.hermes/affiliates/merchants.json before deploy)
const REGISTRY_PATH = new URL('../data/merchants.json', import.meta.url).pathname;

let cachedRegistry: any = null;
let domainIndex: Record<string, string> | null = null;

export type MerchantStatus =
  | 'active'
  | 'pending'
  | 'rejected'
  | 'pending_review'
  | 'dead'
  | 'inactive';

export interface PerSiteEntry {
  status: MerchantStatus;
  affiliateId: string | null;
}

export interface Merchant {
  name: string;
  program: string;
  status: MerchantStatus;
  perSite?: Record<string, PerSiteEntry>;
  commission?: { rate: number; type: string; notes?: string } | null;
  cookieDurationHours?: number | null;
  linkTemplate?: string | null;
  fallbackUrl?: string | null;
  lastVerified?: string;
  notes?: string;
  domainHints?: string[];
}

export interface Registry {
  meta?: {
    version: string;
    lastUpdated: string;
    updatedBy: string;
    source: string;
  };
  merchants: Record<string, Merchant>;
}

export function loadRegistry(): Registry {
  if (cachedRegistry) return cachedRegistry;

  try {
    const raw = readFileSync(REGISTRY_PATH, 'utf-8');
    cachedRegistry = JSON.parse(raw);
    // Build domain→merchantId index
    domainIndex = {};
    for (const [id, merchant] of Object.entries(cachedRegistry.merchants)) {
      const m = merchant as Merchant;
      if (m.domainHints) {
        for (const hint of m.domainHints) {
          domainIndex[hint] = id;
        }
      }
    }
    return cachedRegistry;
  } catch (err) {
    console.warn(
      `[affiliateRegistry] Failed to load registry at ${REGISTRY_PATH}: ${err}`
    );
    return { merchants: {} };
  }
}

export function getMerchant(id: string): Merchant | null {
  const reg = loadRegistry();
  return reg.merchants?.[id] ?? null;
}

export function detectMerchant(url: string): string | null {
  loadRegistry(); // ensure domainIndex is built
  if (!domainIndex) return null;
  const lower = url.toLowerCase();
  for (const [domain, id] of Object.entries(domainIndex)) {
    if (lower.includes(domain)) return id;
  }
  return null;
}

export function canRenderAffiliate(merchantId: string, siteId: string): boolean {
  const merchant = getMerchant(merchantId);
  if (!merchant) return false;

  const perSite = merchant.perSite?.[siteId];
  if (!perSite) return false;

  const status = perSite.status;
  if (['rejected', 'dead', 'inactive'].includes(status)) {
    return false;
  }

  // active, pending, pending_review allowed (if perSite entry exists)
  return true;
}

export function resolveAffiliateUrl(
  merchantId: string,
  siteId: string,
  params: Record<string, string> = {}
): string | null {
  if (!canRenderAffiliate(merchantId, siteId)) {
    return null;
  }

  const merchant = getMerchant(merchantId)!;
  const perSite = merchant.perSite?.[siteId];
  const affiliateId = perSite?.affiliateId ?? '';

  let template = merchant.linkTemplate || merchant.fallbackUrl || '';
  if (!template) {
    return null;
  }

  // Inject affiliateId (common placeholder)
  template = template.replace(/\{affiliateId\}/g, affiliateId);

  // Inject caller-provided params (asin, productId, targetUrl, etc.)
  for (const [key, value] of Object.entries(params)) {
    const re = new RegExp(`\\{${key}\\}`, 'g');
    template = template.replace(re, value);
  }

  return template;
}
