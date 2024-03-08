import { Model } from 'mongoose';
import { Query as QueryType } from 'express-serve-static-core';

export async function paginate<T>(
  model: Model<T>,
  page: QueryType,
  filter: object,
): Promise<any> {
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
