using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace viewer
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            String dir=Directory.GetCurrentDirectory();
            axAcroPDF1.src = dir+"\\network.pdf";
            
        }

        private void axAcroPDF1_Enter(object sender, EventArgs e)
        {
            this.axAcroPDF1.Size = this.ClientSize;

        }
    }
}
