import { Model } from 'mongoose';

export async function paginate<T>(
  model: Model<T>,
  page: any,
  id: any,
  field: any,
): Promise<any> {
  const filter = {};
  filter[field] = id;
  const responsePerPage = 9;
  const currentPage = Number(page) || 1;
  const skip = responsePerPage * (currentPage - 1);
  const totalCount = await model.countDocuments(filter);
  const totalPages = Math.ceil(totalCount / responsePerPage);

  const items = await model.find(filter).limit(responsePerPage).skip(skip);
  if (items.length === 0) {
    throw new Error('No data found');
  }
  return {
    currentPage,
    totalPages,
    totalCount,
    items,
  };
}
