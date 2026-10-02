import React from 'react';

const Card = ({ children, className = '', strong = false }) => {
  return <section className={`${strong ? 'surface-strong' : 'surface'} ${className}`}>{children}</section>;
};

export default Card;
