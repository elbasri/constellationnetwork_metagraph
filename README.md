# Constellation Network Metagraph Integration for Odoo ERP

## Project Description

This project integrates Constellation Network's DAG-based payment method into the Odoo ERP system, enabling secure and transparent transactions. Additionally, it enhances supply chain management using metagraph technology, offering a transparent and efficient way to handle transactions across the supply chain.

## Demo

You can access the live demo of the project at:

**Demo URL:** [https://metagraph.maktab.ma/web](https://metagraph.maktab.ma/web)  
**Username:** demo  
**Password:** nacer

## Video

Watch the project demonstration on YouTube:

**Short Video (4 minutes):** [https://www.youtube.com/watch?v=BxcnlLiw2aU](https://www.youtube.com/watch?v=BxcnlLiw2aU)

**Full Video (22 minutes):** [https://www.youtube.com/watch?v=G5mytFuCvFg](https://www.youtube.com/watch?v=G5mytFuCvFg)

## Installation and Configuration

### Prerequisites

- Odoo 13+ (to odoo 17)
- Python 3.6+
- PostgreSQL

### Steps to Install

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/elbasri/constellationnetwork_metagraph.git
   cd constellationnetwork_metagraph
   ```

**you can also download it directly from odoo apps store (apps.odoo.com):** [https://apps.odoo.com/apps/modules/17.0/constellationnetwork_metagraph](https://apps.odoo.com/apps/modules/17.0/constellationnetwork_metagraph)


2. **Install ODOO:**


   [INSTALL ODOO17 (ARABIC)](https://github.com/elbasri/odoo17)
 

3. **Configure Odoo:**

   Place the module in your Odoo custom addons directory.

   Update your Odoo configuration file (`odoo.conf`) to include the custom addons directory:

   ```ini
   addons_path = /path/to/custom/addons,/path/to/odoo/addons
   ```

4. **Update Odoo:**

   Restart your Odoo instance and update the module list from the Odoo interface. Install the `constellationnetwork_metagraph` module from the Apps menu.

### Configuration

1. **Metagraph Configuration:**

   - Navigate to **Metagraph Management > Configurations**.
   - Configure your wallet addresses and network URLs (Testnet, Integration, Mainnet).

2. **Payment Acquirer Setup:**

   - Go to **Website > Configuration > Payment Acquirers**.
   - Add a new payment acquirer for DAG with the necessary credentials.

### Main Features

- **DAG-based Payments:** 
  - Integration with Constellation Network to handle payments using DAG technology.
  - Supports Testnet, Integration, and Mainnet environments.

- **Supply Chain Transparency:** 
  - Leverages metagraph technology to enhance visibility and traceability in the supply chain.
  - Linked to Sale Orders, Purchase Orders, and Stock Pickings.

- **Graphical Reports:**
  - View metagraph transaction statistics through a visual dashboard within Odoo.

### Code Snippets

**Metagraph Model Example:**
```python
class Metagraph(models.Model):
    _name = 'metagraph'
    _description = 'Metagraph'

    name = fields.Char(string='Metagraph Name', required=True)
    blockchain_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed')
    ], string='Blockchain Status', default='pending')
    transaction_hash = fields.Char(string='Transaction Hash')
    amount = fields.Float(string='Amount')
    # Additional fields and methods...
```

**Transaction Status Check Example:**
```python
def check_status(self):
    api = ConstellationAPI(self._get_base_url(), self._get_faucet_url(), self._get_check_status_url())
    status = self.retry_operation(api.get_metagraph_status, self.transaction_hash)
    if 'data' in status:
        data = status['data']
        self.blockchain_status = 'confirmed'
        self.transaction_hash = data.get('hash')
        # Additional logic...
```

## License

This project is licensed under the LGPL-3 License - see the odoo opensource suported licences file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For any questions or issues, please contact [Abdennacer Elbasri](https://github.com/elbasri).
