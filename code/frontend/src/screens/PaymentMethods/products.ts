class Product {
  constructor(public id: string, public text: string, public isActive: boolean, public price: number) {
    this.id = id;
    this.text = text;
    this.isActive = isActive;
    this.price = price;
  }
}

export const productNormal = new Product("NORMAL_EXAM", "Normál vizsgálat", true, 26990);
export const productPriority = new Product("PRIORITY_EXAM", "Elsőbbségi vizsgálat", true, 36990);

export const products = [productNormal, productPriority];
