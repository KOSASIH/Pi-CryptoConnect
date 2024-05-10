export const truncateString = (str: string, length: number): string => {
  if (str.length > length) {
    return str.substring(0, length) + '...';
  } else {
    return str;
  }
};

export const capitalizeFirstLetter = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const reverseString = (str: string): string => {
  return str.split('').reverse().join('');
};
