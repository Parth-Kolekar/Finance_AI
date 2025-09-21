import Card from '../shared/Card';

const StockCard = ({ name, ticker, price, change, percentage, isPositive, insight }) => {
  return (
    <Card className="flex flex-col justify-between">
      <div>
        <div className="flex justify-between items-baseline">
          <h3 className="text-lg font-semibold text-white">{name}</h3>
          <p className="text-sm text-gray-400 font-mono">{ticker}</p>
        </div>
        <p className="text-3xl font-semibold my-2 text-white">${price}</p>
        <div className={`text-sm font-medium ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
          <span>{change}</span>
          <span className="ml-1">({percentage})</span>
        </div>
      </div>
      <div className="mt-4 pt-4 border-t border-gray-800">
        <p className="text-xs text-gray-500 font-semibold uppercase">AI INSIGHT</p>
        <p className="text-sm text-gray-300 mt-1">{insight}</p>
      </div>
    </Card>
  );
};

export default StockCard;
