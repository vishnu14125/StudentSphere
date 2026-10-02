import React from 'react';

const SectionHeader = ({ title, description, action }) => {
  return (
    <div className="flex items-center justify-between gap-4">
      <div>
        <h2 className="section-title">{title}</h2>
        {description ? <p className="section-copy mt-1">{description}</p> : null}
      </div>
      {action ? <div>{action}</div> : null}
    </div>
  );
};

export default SectionHeader;
