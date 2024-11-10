export function jsonToCamelCase(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map((v) => jsonToCamelCase(v));
  } else if (obj !== null && obj.constructor === Object) {
    return Object.keys(obj).reduce((acc, key) => {
      const camelCaseKey = key.replace(/_([a-z])/g, (_, char) => char.toUpperCase());
      acc[camelCaseKey] = jsonToCamelCase(obj[key]);
      return acc;
    }, {} as any);
  }
  return obj;
}

export function capitalise(s: string) {
  return String(s[0]).toUpperCase() + String(s).slice(1);
}

export const PRICE_REGEX = /^\d+(\.\d{1,2})?$/;