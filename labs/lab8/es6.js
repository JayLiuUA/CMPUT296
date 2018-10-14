class Complex3 {
  constructor(real, imag) {
    this.real = real;
    this.imag = imag;
  }

  magnitude() {
    return Math.sqrt(this.real ** 2 + this.imag ** 2);
  }
}
