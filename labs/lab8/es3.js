function Complex1(real, imag) {
  this.real = real;
  this.imag = imag;
}
Complex1.prototype.magnitude = function() {
  return Math.sqrt(this.real ** 2 + this.imag ** 2);
};
