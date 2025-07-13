const FollowUpList = ({ suggestions, onSelect }) => {
  return (
    <div className="followup-list">
      {suggestions?.map((item, idx) => (
        <button
          key={idx}
          className="followup-chip"
          onClick={() => onSelect(item)}
        >
          {item}
        </button>
      ))}
    </div>
  );
};
