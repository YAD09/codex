export const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.8, ease: 'easeOut' } },
};

export const slideUp = {
  hidden: { opacity: 0, y: 32 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: 'easeOut' } },
};

export const staggerChildren = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.15,
    },
  },
};

export const hoverGlow = {
  rest: {
    boxShadow: '0 0 0 rgba(64,243,255,0)',
    scale: 1,
  },
  hover: {
    boxShadow: '0 0 30px rgba(64,243,255,0.45)',
    scale: 1.02,
    transition: { duration: 0.3, ease: 'easeOut' },
  },
};
